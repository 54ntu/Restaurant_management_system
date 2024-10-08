from django.urls import path,include
from .views import (CategoryViewstets, TableViewsets, MenuItemViewset, OrderViewset,CartView,CartItemViewset,)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'category',CategoryViewstets)
router.register(r'table',TableViewsets)
router.register(r'menuItem', MenuItemViewset)
router.register(r'carts',CartView)
router.register(r'cart-items',CartItemViewset)
router.register(r'order', OrderViewset)


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
