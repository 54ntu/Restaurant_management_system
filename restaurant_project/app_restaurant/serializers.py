from rest_framework import serializers
from .models import Category,Table,MenuItem,Order,OrderItem,Cart,CartItem
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =('id',"name",)



class TableSerializer(serializers.ModelSerializer):
    managed_by= serializers.StringRelatedField(read_only=True)
    # managed_by_id = serializers.PrimaryKeyRelatedField(
    #     queryset = User.objects.all(), source="managed_by"
    # )
    class Meta:
        model = Table
        fields = ['id', 'table_no', 'capacity',
                  'availability_status', 'managed_by',]


class MenuItemSerializer(serializers.ModelSerializer):
        category= serializers.StringRelatedField()
        category_id= serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category')
        class Meta:
            model = MenuItem
            fields = ['id', 'category', 'category_id', 'name',
                      'price', 'item_availability']



class OrderItemSerializer(serializers.ModelSerializer):
     order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
     menu_item_id= serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(),source="Menu_item" )
     menus = MenuItemSerializer()

     class Meta:
          model = OrderItem
          fields =['id','order_id','menu_item_id','menus','quantity','item_price']
    

class OrderSerializer(serializers.ModelSerializer):
     order_items = OrderItemSerializer(many=True)
     table_assigned = serializers.PrimaryKeyRelatedField(
         queryset=Table.objects.all())
     order_taken_by = serializers.PrimaryKeyRelatedField(
         queryset=User.objects.all())
     #source="val" is required only if the attributes of table and attributes of serializer fields are different otherwise it should not be written
     
     
     class Meta:
          model= Order
          fields=['id','table_assigned','order_items','order_taken_by','order_status','created_at','total_price']



class CreateOrderSerializer(serializers.ModelSerializer):
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     delivery_address = serializers.CharField()

     class Meta:
          model = Order
          fields=[
               'id',
               'user',
               'delivery_address',
          ]


     def create(self, validated_data):
          user = validated_data.pop('user')
          cart = Cart.objects.get(user = validated_data.get('user'))
          cart_items = CartItem.objects.filter(cart=cart)
          order = Order.objects.create(user=user,**validated_data)
          order_items_objects=[]
          for item in cart_items:
               order_item = OrderItem(
                    order= order,
                    menuItem = item.menuItem,
                    quantity = item.quantity,
                    price = item.total_menuItem_price
               )
          order_items_objects.append(order_item)
          OrderItem.objects.bulk_create(order_items_objects)
          cart.delete()
          Cart.objects.get_or_create(user=validated_data.get('user'))
          return order

class CartItemSerializer(serializers.ModelSerializer):
     cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(),source="cart" )
     MenuItem_id = serializers.PrimaryKeyRelatedField(
         queryset=MenuItem.objects.all(), source="menuItem")
     menuItem = MenuItemSerializer()

     class Meta:
          model = CartItem
          fields = ('id', 'cart_id', 'MenuItem_id',
                    'menuItem', 'quantity', 'total_menuItem_price')


class CartSerializer(serializers.ModelSerializer):
     user_id = serializers.PrimaryKeyRelatedField(queryset= User.objects.all(),source="user")
     user = serializers.StringRelatedField()
     cart_items = CartItemSerializer(many=True)


     class Meta:
          model = Cart
          fields = ('id', 'user_id','user','cart_items','total_bill',)


class AddToCartSerializer(serializers.ModelSerializer):
     user = serializers.HiddenField(default = serializers.CurrentUserDefault())
     menuItem_id = serializers.PrimaryKeyRelatedField(queryset = MenuItem.objects.all(),source= "menuItem")

     class Meta:
          model = CartItem
          fields =('id','user','menuItem_id','quantity',)
     
     def create(self, validated_data):
          user = validated_data.pop('user')
          cart,_ = Cart.objects.get_or_create(user=user)
          try:
               cart_item = CartItem.objects.get(cart__user=user,menuItem= validated_data.get('menuItem'))
               cart_item.quantity+= validated_data.get('quantity')
               cart_item.save()
          except CartItem.DoesNotExist:
              #if the cartItem is not available ,create a new cart item
              validated_data['cart']= cart
          return super().create(validated_data)
    