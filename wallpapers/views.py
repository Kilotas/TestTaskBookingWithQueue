from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, QueueEntry
from .utils import is_slot_available, add_to_queue, release_slot
from .serializers import BookingSerializer, QueueEntrySerializer


class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingSerializer

    @extend_schema(
        request=BookingSerializer,
        responses={
            201: {
                'description': 'Booking created successfully',
                'schema': BookingSerializer,
            },
            400: {
                'description': 'Invalid data or slot unavailable',
            },
        },
        summary='Create a booking',
        description='Create a new booking for a resource. If no slots are available, add the user to the queue.'
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resource = serializer.validated_data['resource']
        start_time = serializer.validated_data['start_time']

        # Check slot availability
        if not is_slot_available(resource, start_time):  # Adjust this function as necessary
            add_to_queue(request.user, resource)
            return Response(
                {"detail": "Все слоты заняты. Вы добавлены в очередь."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save the booking
        booking = serializer.save(user=request.user)
        return Response(self.get_serializer(booking).data, status=status.HTTP_201_CREATED)


class BookingDeleteAPIView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'  # Assuming 'id' is the primary key field

    @swagger_auto_schema(
        responses={
            204: 'Booking deleted successfully',
            404: 'Booking not found',
        },
        summary='Delete a booking',
        description='Delete a booking by its ID and release the associated slot.'
    )

    def perform_destroy(self, instance):
        release_slot(instance)
        instance.delete()

class BookingListAPIView(generics.ListAPIView):
    """
      API endpoint that allows users to view all their bookings.
      """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @extend_schema(
        operation_id="list_bookings",
        responses={
            200: BookingSerializer(many=True),
        },
        description="Retrieve a list of all bookings, including active and queued.",
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve all bookings.
        """
        return super().get(request, *args, **kwargs)

class QueueListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QueueEntrySerializer

    @extend_schema(
        responses=QueueEntrySerializer,
        summary='Get user queue entries',
        description='Retrieve the queue entries for the authenticated user.'
    )
    def get_queryset(self):
        # Возвращаем только записи очереди для текущего пользователя
        return QueueEntry.objects.filter(user=self.request.user, booking__isnull=True).order_by('created_at')


class BookingCancelAPIView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()

        # Отменяем бронирование
        booking.status = 'completed'
        booking.save()

        # Проверяем, есть ли пользователи в очереди
        next_queue_entry = QueueEntry.objects.filter(booking__isnull=True).order_by('created_at').first()
        if next_queue_entry:

            new_booking = Booking.objects.create(
                user=next_queue_entry.user,
                resource=booking.resource,
                start_time=booking.start_time,
                end_time=booking.end_time,
                status='active'  # или другое значение для активного бронирования
            )
            # Удаляем запись из очереди
            next_queue_entry.booking = new_booking
            next_queue_entry.save()

            # Уведомляем следующего пользователя (здесь можно использовать сигнал или просто вывести сообщение)
            print(f"Уведомление: {next_queue_entry.user.username}, ваш слот был активирован!")

        return Response(status=status.HTTP_204_NO_CONTENT)





