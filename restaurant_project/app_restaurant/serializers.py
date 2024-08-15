from rest_framework import serializers
from .models import Category,Table,MenuItem
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




class OrderSerializer(serializers.ModelSerializer):
     pass