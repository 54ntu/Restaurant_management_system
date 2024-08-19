from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Category, Table, MenuItem, Order, OrderItem, Cart, CartItem
from .serializers import (CategorySerializer, TableSerializer, MenuItemSerializer, OrderSerializer,
                          OrderItemSerializer, CartSerializer, CartItemSerializer, AddToCartSerializer,)
from .permissions import IsAdminOrReadOnly

# Create your views here.


class CategoryViewstets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # here normal users like waiter or reception doesnot has the power to add or update or delete
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)


class TableViewsets(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # automatically set the  managed_by  field to  the currently  logged in user
        serializer.save(managed_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # this one will filter out the data related to the logged in user
        return Table.objects.filter(managed_by=user)


class MenuItemViewset(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]


class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartView(GenericViewSet, ListAPIView):
    queryset = Cart.objects.prefetch_related("cart_items").all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        print(f"current logged in user is :{user}")
        return self.queryset.filter(user= user)


class CartItemViewset(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes= (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method =="POST":
            return AddToCartSerializer
        return CartItemSerializer
    

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(cart__user= user)

