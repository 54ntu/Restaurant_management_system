from django.contrib import admin
from .models import Category,MenuItem,Order,Table,OrderItem,Cart,CartItem

# Register your models here.
@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display=('id','name',)
@admin.register(Table)
class TableAdminModel(admin.ModelAdmin):
    list_display = ('id', 'table_no', 'capacity',
                    'availability_status', 'managed_by')

@admin.register(MenuItem)
class MenuItemAdminModel(admin.ModelAdmin):
    list_display = ('id','category','name','price','item_availability')


class OrderItemInline(admin.TabularInline): 
    model = OrderItem
    extra = 3




@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ('id', 'table_assigned', 'order_taken_by',
                    'order_status', 'created_at', 'updated_at',)
    inlines = (OrderItemInline,)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra=2


@admin.register(Cart)
class CartAdminModel(admin.ModelAdmin):
    list_display = ('id','user',)
    inlines = (CartItemInline,)
