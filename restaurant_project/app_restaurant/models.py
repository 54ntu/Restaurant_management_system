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
    OCCUPPIED_STATS = "OCCUPPIED"
    AVAILABLE_STATS = "AVAILABLE"
    
    AVAILABILITY_CHOICES= [
        (OCCUPPIED_STATS, 'OCCUPPIED'),
        (AVAILABLE_STATS, 'AVAILABLE'),
    ]
    
    table_no= models.PositiveIntegerField(unique=True)
    capacity= models.PositiveIntegerField()
    availability_status = models.CharField(choices=AVAILABILITY_CHOICES,max_length=20)
    managed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_managed')


class MenuItem(models.Model):
     category = models.ForeignKey(Category,on_delete=models.CASCADE)
     name=models.CharField(max_length=100,)
     price = models.DecimalField(max_digits=10,decimal_places=2)
     item_availability=models.BooleanField(default=True)

     def __str__(self):
        return self.name 



class Order(models.Model):
    PENDING_CHOICE = "PENDING"
    DELIVERED_CHOICE = "DELIVERED"
    CANCELLED_CHOICE = "CANCELLED"

    ORDER_STATUS =[
        (DELIVERED_CHOICE, 'DELIVERED'),
        (CANCELLED_CHOICE, 'CANCELLED'),
        (PENDING_CHOICE, 'PENDING'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_assigned= models.ForeignKey(Table,on_delete=models.CASCADE)
    order_taken_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders_taken')
    order_status = models.CharField(choices=ORDER_STATUS,max_length=50)
    payment_status= models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)



    @property
    def total_price(self):
        total_amount= 0
        for item in self.order_items.all():
            total_amount = total_amount+ item.price
        return total_amount


class OrderItem(models.Model):
    # In Django's ORM, the related_name attribute in a ForeignKey field defines the name of the reverse relation from the related model back to the model that defines the foreign key.
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10 , decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} ({self.quantity})"
    
    @property
    def item_price(self):
        return self.quantity* self.menu_item.price

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)


    @property
    def total_bill(self):
        total_amount = 0
        for item in self.cart_items.all():
            total_amount = total_amount + item.total_menuItem_price
        return total_amount
    
    @property
    def subTotal_items(self):
        total_items = 0
        for item in self.cart_items.all():
            total_items = total_items+item.quantity
        return total_items



class CartItem(models.Model):
    cart= models.ForeignKey(Cart,on_delete=models.CASCADE, related_name="cart_items")
    menuItem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    @property
    def total_menuItem_price(self):
        return self.quantity * self.menuItem.price