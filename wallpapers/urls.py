from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import QueueListAPIView, BookingCreateAPIView, BookingDeleteAPIView, BookingListAPIView, BookingCancelAPIView

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/<int:booking_id>/', BookingDeleteAPIView.as_view(), name='booking-delete'),
    path('queue/', QueueListAPIView.as_view(), name='queue'),
    path('api/bookings/', BookingListAPIView.as_view(), name='api-bookings-create'),
    path('bookings/cancel/<int:pk>/', BookingCancelAPIView.as_view(), name='booking-cancel'),
]




