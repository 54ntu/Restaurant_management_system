from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,)

    def __str__(self):
        return self.name
    

class Table(models.Model):
    AVAILABILITY_CHOICES= [
        ('occuppied','OCCUPPIED'),
        ('available', 'AVAILABLE'),


    ]
    table_no= models.PositiveIntegerField(unique=True)
    capacity= models.PositiveIntegerField()
    availability_status = models.CharField(choices=AVAILABILITY_CHOICES,max_length=20)
    managed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_managed')

    def __str__(self):
        return self.table_no +self.availability_status
    


class MenuItem(models.Model):
     category = models.ForeignKey(Category,on_delete=models.CASCADE)
     name=models.CharField(max_length=100,)
     price = models.DecimalField(max_digits=10,decimal_places=3)
     item_availability=models.BooleanField(default=False)

     def __str__(self):
        return self.name 
     


class Order(models.Model):
    ORDER_STATUS =  [
        ('delivered','DELIVERED'),
        ('cancelled','CANCELLED'),
        ('pending', 'PENDING'),

    ]
    table_assigned= models.ForeignKey(Table,on_delete=models.CASCADE)
    order_taken_by =models.ForeignKey(User,on_delete=models.CASCADE)
    order_status = models.CharField(choices=ORDER_STATUS,max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10 , decimal_places=2)




    def __str__(self):
        return self.quantity + self.menu_item.name