from django.urls import path,include
from .views import CategoryViewstets, TableViewsets
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'category',CategoryViewstets)
router.register(r'table',TableViewsets)

urlpatterns = [
    # path('category/',CategoryViewstets.as_view({
    #     'get':'list',
    #     'post':'create'
    # })),
    # path('tableViewsets/', TableViewsets.as_view({
    #     'get': 'list',
    #     'post': 'perform_create'
    # })),

    path('', include(router.urls))



]
