from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('InventorymanagementProduct/',      ProductListView.as_view(),   name='InventorymanagementProduct'),
    path('InventorymanagementProduct/<int:pk>/', ProductDetailView.as_view(), name='InventorymanagementProduct-detail'),
    
]