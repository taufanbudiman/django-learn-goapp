import time

import pandas as pd
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

from main.apps.order.models import BulkProducts, Products, Orders, OrderDetails
from main.settings import BASE_DIR


@shared_task()
def upload_process_job():
    data = BulkProducts.objects.filter(status=BulkProducts.PENDING).first()
    if data:
        data.mark_processing()
        file_path = data.file.path
        df = pd.read_csv(file_path)
        count = len(df)
        i = 1
        for index, row in df.iterrows():
            product = Products(
                name=row['Name'],
                price=row['Price'],
                sku=row['SKU'],
                stock=row['Stock'],
            )
            product.save()
            data.progress = (i / count) * 100
            data.save()
            i += 1
            # send notify to client with websocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'upload', {"type": "notify", "message": {
                    'id': data.id,
                    'progress': data.progress,
                }}
            )
            time.sleep(2)

        data.mark_done()
        return 'job done'


@shared_task()
@transaction.atomic
def update_order_job(data: dict):
    order_data = {
        'order_id': data.get('order_id'),
        'marketplace': data.get('marketplace'),
        'total_price': data.get('amt')['ttl_amount'],
    }
    order, _ = Orders.objects.update_or_create(
        order_number=data.get('invoice_num'),
        create_defaults=order_data,
    )
    order.save()
    for product_serialize in data.get('products'):
        product = Products.objects.get(sku=product_serialize.get('sku'))
        order_detail_data = {
            'quantity': product_serialize.get('quantity'),
            'price': product_serialize.get('price'),
            'total_price': product_serialize.get('total_price'),
        }
        order_detail, _ = OrderDetails.objects.update_or_create(
            order=order,
            product=product,
            create_defaults=order_detail_data,
        )
        order_detail.save()
    return f"""
    Successfully add product with SKU  
    {', '.join(p.get('sku') for p in data.get('products'))}
    """


def create_dummy_product():
    i = 1
    list_of_products = []
    while i <= 100:
        list_of_products.append([
            f'Product {i:04}',
            f'SKU{i:04}',
            100000,
            100
        ]
        )
        i += 1

    df = pd.DataFrame(list_of_products, columns=[
        'Name', 'SKU', 'Price', 'Stock'])
    df.to_csv(BASE_DIR / 'products.csv', index=False)


def test_send_message():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'upload', {"type": "notify", "message": 'candu'}
    )
    return async_to_sync(channel_layer.group_send)(
        'upload', {"type": "notify", "message": 'iya'}
    )
