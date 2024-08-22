from rest_framework import serializers
from .models import Category, Table, MenuItem, Order, OrderItem, Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', "name",)


class TableSerializer(serializers.ModelSerializer):
    managed_by = serializers.StringRelatedField(read_only=True)
    # managed_by_id = serializers.PrimaryKeyRelatedField(
    #     queryset = User.objects.all(), source="managed_by"
    # )

    class Meta:
        model = Table
        fields = ['id', 'table_no', 'capacity',
                  'availability_status', 'managed_by',]


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category')

    class Meta:
        model = MenuItem
        fields = ['id', 'category', 'category_id', 'name',
                  'price', 'item_availability']


class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source="menu_item")
    menu_item = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'menu_item_id',
                  'menu_item', 'quantity', 'item_price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True,read_only=True)
    table_assigned = serializers.SerializerMethodField()
    order_taken_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    # source="val" is required only if the attributes of table and attributes of serializer fields are different otherwise it should not be written

    class Meta:
        model = Order
        fields = ['id', 'order_items', 'table_assigned', 'payment_status',
                  'order_taken_by', 'order_status', 'created_at', 'total_price',]
        
    
    def get_table_assigned(self,obj):
        print(f"table value is {obj.table_assigned}")
        return obj.table_assigned.table_no


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    table_no = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'table_no',
        ]


    def validate_table_no(self, value):
        try:
            table=Table.objects.get(table_no=value)
        except Table.DoesNotExist:
            raise serializers.ValidationError("table with this number does not exist")
        if table.availability_status == Table.OCCUPPIED_STATS:
            raise serializers.ValidationError("this table is currently occupied")
        return table
    
    def validate(self, attrs):
        user = self.context['request'].user
        print(f"user value is : {user}")
        cart = Cart.objects.filter(user=user).first()

        #check whether the cart exists and has items on it
        if not cart or not  CartItem.objects.filter(cart=cart).exists():
            raise serializers.ValidationError("your cart is empty. please add items to the cart before placing an order....!!")
        return attrs

    def create(self, validated_data):
        user = validated_data.pop('user')
        table_assigned = validated_data.get('table_no')
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        # create the order and set the order_taken_by field to the current user
        order = Order.objects.create(
            user=user,
            table_assigned=table_assigned,
            order_taken_by=user,
            order_status= Order.PENDING_CHOICE
        )
        # creating order
        order_items_objects = []
        for item in cart_items:
            order_item = OrderItem(
                order_id=order,
                menu_item=item.menuItem,
                quantity=item.quantity,
                price=item.total_menuItem_price
            )
            order_items_objects.append(order_item)
        OrderItem.objects.bulk_create(order_items_objects)

        #change the avaialable status of table to occupied
        table_assigned.availability_status = Table.OCCUPPIED_STATS
        table_assigned.save()
        cart.delete()
        Cart.objects.get_or_create(user=user)
        return order


class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = []

    def update(self, instance: Order, validated_data):
        instance.order_status = Order.CANCELLED_CHOICE
        #access the assigned table 
        table= instance.table_assigned
        table.availability_status= Table.AVAILABLE_STATS
        table.save()
        instance.save()
        return instance


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields =['order_status',]


class UpdatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields =['payment_status',]



    def update(self, instance:Order, validated_data):
        instance.payment_status = Order.payment_status
        table = instance.table_assigned
        table.availability_status = Table.AVAILABLE_STATS
        table.save()
        instance.delete()
        return instance
    
    

class CartItemSerializer(serializers.ModelSerializer):
    cart_id = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), source="cart")
    MenuItem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source="menuItem")
    menuItem = MenuItemSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'cart_id', 'MenuItem_id',
                  'menuItem', 'quantity', 'total_menuItem_price')


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user")
    user = serializers.StringRelatedField()
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user_id', 'user', 'cart_items',
                  'total_bill', 'subTotal_items',)


class AddToCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menuItem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source="menuItem")

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'menuItem_id', 'quantity',)

    def create(self, validated_data):
        user = validated_data.pop('user')
        cart, _ = Cart.objects.get_or_create(user=user)
        try:
            # check if the cart-item already exists
            cart_item = CartItem.objects.get(
                cart=cart, menuItem=validated_data.get('menuItem'))
            # if exist just increase the quantity
            cart_item.quantity += validated_data.get('quantity')
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            # if the cartItem is not available ,create a new cart item
            validated_data.update({
                "cart": cart,
            })
        return super().create(validated_data)
