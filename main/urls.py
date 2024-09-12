"""
URL configuration for goapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.apps.order import views

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', views.ProductListView.as_view(),
         name='product_list_view'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(),
         name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(),
         name='product_create'),
    path('bulk-products/', views.BulkProductListView.as_view(),
         name='bulk_product_list_view'),
    path('bulk-products/add/', views.BulkProductCreateView.as_view(),
         name='bulk_product_create'),
    path('main-serive/api/v1/ordernotification',
         views.webhook_order_notification,
         name='webhook_order_notification'),
]
