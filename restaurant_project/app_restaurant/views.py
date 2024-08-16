from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Category,Table,MenuItem,Order,OrderItem
from .serializers import CategorySerializer,TableSerializer,MenuItemSerializer,OrderSerializer,OrderItemSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response

# Create your views here.
class CategoryViewstets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,IsAdminOrReadOnly) # here normal users like waiter or reception doesnot has the power to add or update or delete



class TableViewsets(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        #automatically set the  managed_by  field to  the currently  logged in user
        serializer.save(managed_by= self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Table.objects.filter(managed_by=user) # this one will filter out the data related to the logged in user



class MenuItemViewset(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]


class OrderViewset(ModelViewSet):
    queryset= Order.objects.all()
    serializer_class = OrderSerializer
    
    