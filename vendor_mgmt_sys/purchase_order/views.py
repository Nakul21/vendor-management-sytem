# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer, UpdatePurchaseOrderSerializer
from django.db import transaction
from datetime import datetime
from django.utils import timezone
from .signals import temporarily_disable_signals, reconnect_signals
from django.db.models import Avg, F, ExpressionWrapper, fields


class PurchaseOrderCreateAPIView(APIView):

    def post(self, request, format=None):
        """
        Create a new purchase order.

        Parameters:
        - request: HTTP request object
        - format: Optional string specifying the requested format (e.g., 'json')

        Returns:
        - HTTP response with created purchase order data if successful,
          or error response if failed.
        """
        try:
            serializer = PurchaseOrderSerializer(data=request.data)

            # Validate input data
            if serializer.is_valid():
                serializer.save()
                return Response({"data": f"Vendor's {serializer.data.get('vendor')}, purchase order {serializer.data.get('po_number')} created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(exception=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, format=None):
        """
        API endpoint to list all purchase orders with an option to filter by vendor.

        This endpoint allows clients to retrieve a list of all purchase orders.
        Clients can also filter the purchase orders by specifying a vendor ID in the
        query parameters.

        Example usage:
        GET /api/purchase_orders/
        GET /api/purchase_orders/?vendor_id=1
        """
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

class PurchaseOrderDetailAPIView(APIView):
    """
    API endpoint to retrieve, update, or delete a specific purchase order.

    This endpoint allows clients to retrieve, update, or delete details of a
    specific purchase order identified by its unique ID.

    Example usage:
    GET    /api/purchase_orders/{po_id}/
    PUT    /api/purchase_orders/{po_id}/
    DELETE /api/purchase_orders/{po_id}/
    """

    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(po_number=po_id)
        except PurchaseOrder.DoesNotExist:
            return None

    def get(self, request, po_id, format=None):
        purchase_order = self.get_object(po_id)
        if purchase_order:
            serializer = UpdatePurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        else:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, po_id, format=None):
        purchase_order = self.get_object(po_id)
        if purchase_order:
            with transaction.atomic():
                po_update = PurchaseOrder.objects.select_for_update().get(po_number=purchase_order.po_number)
                for key, value in request.data.items():
                    setattr(po_update, key, value)
                po_update.save()
                return Response({"message": f"Successfully update {po_update.po_number} for vendor {po_update.vendor}", "status": True}, status=status.HTTP_200_OK)                
        else:
            return Response({"message": f"Failed to update {po_id}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id, format=None):
        purchase_order = self.get_object(po_id)
        if purchase_order:
            purchase_order.delete()
            return Response({'message': 'Purchase order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)
        
class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id, format=None):
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update acknowledgment_date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response({"message": f"Acknowledgment date updated for purchase order {po_id} and average_response_time recalculated."},
                        status=status.HTTP_200_OK)