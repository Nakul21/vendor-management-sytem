from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VendorSerializer
from .models import Vendor
from django.shortcuts import get_object_or_404

import jwt
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timedelta

def generate_token(request):
    # Define the payload for the token
    payload = {
        'app_name': 'vendor_mgmt_sys',
        'exp': datetime.utcnow() + timedelta(minutes=25)
    }

    try:
        # Generate the token using the payload and your secret key
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({"token": token}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)



class VendorCreateAPIView(APIView):
    """
    View to creat Vendors in the application
    """
    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{serializer.data.get('vendor_code')} created successfully", "status": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorListAPIView(APIView):
    """
    View to list all the vendors that are there in the database
    """
    def get(self, request, format=None):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    

class VendorRetrieveAPIView(APIView):
   """
   View to get the details of a specific vendor
   """
   def post(self, request, format=None):
        data = request.data
        vendor_data = Vendor.objects.filter(vendor_code=data.get("vendor_code")).first()
        serializer = VendorSerializer(vendor_data)
        return Response(serializer.data)

class VendorUpdateAPIView(APIView):
    """
    API endpoint to update a vendor's details.

    Parameters:
    - vendor_code (str): The unique identifier of the vendor.

    Methods:
    - put: Update the details of the vendor with the specified vendor code.
    """

    def put(self, request, vendor_code, format=None):
        """
        Update the details of a vendor.

        Args:
        - request (Request): The HTTP request object.
        - vendor_code (str): The unique identifier of the vendor.
        - format (str, optional): The format of the response.

        Returns:
        - Response: HTTP response indicating the result of the update operation.
        """
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Vendor profile with vendor code {vendor_code} updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorDeleteAPIView(APIView):
    """
    API endpoint to delete a vendor.

    Parameters:
    - vendor_id (int): The unique identifier of the vendor.

    Methods:
    - delete: Delete the vendor record with the specified vendor ID.
    """

    def delete(self, request, vendor_code, format=None):
        """
        Delete a vendor record.

        Args:
        - request (Request): The HTTP request object.
        - vendor_id (int): The unique identifier of the vendor.
        - format (str, optional): The format of the response.

        Returns:
        - Response: HTTP response indicating the result of the delete operation.
        """
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        vendor.delete()
        return Response({"message": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class VendorPerformanceView(APIView):
    """
    Endpoint to retrieve performance metrics for a specific vendor.

    GET /api/vendors/{vendor_id}/performance

    Parameters:
    - vendor_id: The ID of the vendor for which performance metrics are requested.

    Returns:
    - JSON response containing the performance metrics for the specified vendor.
    """

    def get(self, request, vendor_code ):
        try:
            # Retrieve the vendor instance
            vendor = get_object_or_404(Vendor, vendor_code=vendor_code)

            # Calculate performance metrics
            performance_metrics = {
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate
            }

            # Return the performance metrics
            return Response({"message": performance_metrics}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)