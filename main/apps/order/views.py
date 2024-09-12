from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.apps.order.models import Products, BulkProducts, Orders, OrderDetails
from main.apps.order.serializers import OrderNotificationSerializer
from .tasks import update_order_job


# Create your views here.
class ProductListView(ListView):
    model = Products
    template_name = 'product_list.html'
    ordering = ['sku']


class ProductDetailView(DetailView):
    model = Products
    template_name = 'product_detail.html'


class ProductCreateView(CreateView):
    model = Products
    fields = '__all__'
    template_name = 'product_create.html'
    success_url = '/products/'


class BulkProductListView(ListView):
    model = BulkProducts
    template_name = 'bulk_product.html'


class BulkProductCreateView(CreateView):
    model = BulkProducts
    fields = ['file', 'status']
    template_name = 'bulk_product_create.html'
    success_url = '/bulk-products/'


# Create your views here.
@api_view(['POST'])
def webhook_order_notification(request):
    request.data['marketplace'] = 'tokopedia'
    serializer = OrderNotificationSerializer(data=request.data)
    if serializer.is_valid():
        update_order_job.delay(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


