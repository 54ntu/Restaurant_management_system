from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Category,Table
from .serializers import CategorySerializer,TableSerializer
from .permissions import IsAdminOrReadOnly

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
        serializer.save(managed_by= self.request.user,managed_by_id = self.request.user.id)

    def get_queryset(self):
        user = self.request.user
        return Table.objects.filter(managed_by=user) # this one will filter out the data related to the logged in user
