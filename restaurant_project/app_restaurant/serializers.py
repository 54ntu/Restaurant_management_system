from rest_framework import serializers
from .models import Category,Table,MenuItem,Order,OrderItem
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
     order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(),source="order_id")
     menu_item_id= serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(),source="Menu_item" )
     menus = MenuItemSerializer()

     class Meta:
          model = OrderItem
          fields =['id','order_id','menu_item_id','menus','quantity','price']
    

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