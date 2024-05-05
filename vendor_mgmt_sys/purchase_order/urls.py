# urls.py
from django.urls import path
from .views import PurchaseOrderCreateAPIView, PurchaseOrderDetailAPIView, AcknowledgePurchaseOrderAPIView

urlpatterns = [
    path('api/purchase_orders/', PurchaseOrderCreateAPIView.as_view(), name='purchase_order-create-list'),
    path('api/purchase_orders/<str:po_id>', PurchaseOrderDetailAPIView.as_view(), name='vendor-list'),
    path('api/purchase_orders/<str:po_id>/acknowledge', AcknowledgePurchaseOrderAPIView.as_view(), name='vendor-acknowledgment')
]
