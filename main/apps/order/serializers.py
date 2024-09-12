from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    Name = serializers.CharField()
    sku = serializers.CharField()
    price = serializers.IntegerField()
    total_price = serializers.IntegerField()
    quantity = serializers.IntegerField()


class AmountTotalSerializer(serializers.Serializer):
    ttl_product_price = serializers.IntegerField()
    ttl_amount = serializers.IntegerField()


class OrderNotificationSerializer(serializers.Serializer):
    invoice_num = serializers.CharField()
    order_id = serializers.CharField()
    marketplace = serializers.CharField()
    products = ProductSerializer(many=True)
    amt = AmountTotalSerializer()
