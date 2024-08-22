from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Category, Table, MenuItem, Order, OrderItem, Cart, CartItem
from .serializers import (CategorySerializer, TableSerializer, MenuItemSerializer, OrderSerializer,
                          OrderItemSerializer, CartSerializer, CartItemSerializer, AddToCartSerializer, 
                          CreateOrderSerializer, CancelOrderSerializer, UpdateOrderSerializer, UpdatePaymentSerializer)
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import SAFE_METHODS
from django.db.models import Prefetch
from rest_framework.response import Response

# Create your views here.


class CategoryViewstets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # here normal users like waiter or reception doesnot have the power to add or update or delete
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)


class TableViewsets(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly,]

    def perform_create(self, serializer):
        # automatically set the  managed_by  field to  the currently  logged in user
        serializer.save(managed_by=self.request.user)

    def get_queryset(self):
        # user = self.request.user
        # this one will filter out the data related to the logged in user
        return Table.objects.all()


class MenuItemViewset(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]


class OrderViewset(ModelViewSet):
    queryset = Order.objects.prefetch_related(Prefetch(
        "order_items", queryset=OrderItem.objects.all(), to_attr="items")).all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(order_taken_by=user)
    # this line of code filter out the order according to the logged in waiter or reception

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderSerializer
        if self.request.method in ['PUT', 'PATCH']:
            # print(f"self.request.data value is : {self.request.data}")
            if 'order_status' in self.request.data:
                print(
                    f"order status value is : {self.request.data.get('order_status')}")
                if self.request.data.get('order_status') == Order.CANCELLED_CHOICE:
                    print(f"cancelorderserializer is executed..!!")
                    return CancelOrderSerializer
                print("updateorderserializer is called...")
                return UpdateOrderSerializer
            if 'payment_status' in self.request.data:
                print(f"update payment serializer is called...!!!")
                return UpdatePaymentSerializer
        return CreateOrderSerializer


class CartView(GenericViewSet, ListAPIView):
    queryset = Cart.objects.prefetch_related("cart_items").all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        print(f"current logged in user is :{user}")
        return self.queryset.filter(user=user)


class CartItemViewset(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddToCartSerializer
        return CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(cart__user=user)
