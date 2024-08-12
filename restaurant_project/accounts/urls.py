from django.urls import path
from .views import RegisterUserViewsets

urlpatterns = [
    path('register',RegisterUserViewsets.as_view({
        'post':'create'
    })),
]
