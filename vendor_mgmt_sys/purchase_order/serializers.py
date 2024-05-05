# serializers.py
from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class UpdatePurchaseOrderSerializer(serializers.Serializer):
    po_number = serializers.CharField(allow_blank=True)
    order_date = serializers.DateField(required=False)
    delivery_date = serializers.DateField(required=False)
    status = serializers.CharField(allow_blank=True)
    quality_rating = serializers.CharField(allow_blank=True)
    acknowledgment_date = serializers.DateField(required=False)