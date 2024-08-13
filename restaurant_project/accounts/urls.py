from django.urls import path
from .views import UserViewsets

urlpatterns = [
    path('register', UserViewsets.as_view({
        'post':'create'
    })),
    path('login', UserViewsets.as_view({
         'post': 'login'
         })),
]
