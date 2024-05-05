# urls.py
from django.urls import path
from .views import VendorCreateAPIView, VendorListAPIView, VendorRetrieveAPIView, VendorUpdateAPIView, VendorDeleteAPIView, VendorPerformanceView, generate_token

urlpatterns = [
    path('generate-token/', generate_token, name='generate_token'),
    path('api/vendors/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('api/vendors/list', VendorListAPIView.as_view(), name='vendor-list'),
    path('api/fetch_vendor_info', VendorRetrieveAPIView.as_view(), name='vendor-detail'),
    path('api/vendors/<str:vendor_code>/', VendorUpdateAPIView.as_view(), name='vendor-retrieve-update'),
    path('api/vendors/delete/<str:vendor_code>/', VendorDeleteAPIView.as_view(), name='vendor_delete'),
    path('api/vendors/<str:vendor_code>/performance', VendorPerformanceView.as_view(), name='vendor_performance')
]
