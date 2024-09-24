from rest_framework import serializers

from rest_framework import serializers
from .models import Booking, QueueEntry

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'resource', 'start_time', 'end_time', 'status']

    def validate(self, attrs):
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError("Время начала должно быть меньше времени окончания.")

        existing_bookings = Booking.objects.filter(
            resource=attrs['resource'],
            start_time__lt=attrs['end_time'],
            end_time__gt=attrs['start_time']
        )

        if existing_bookings.exists():
            raise serializers.ValidationError("Этот ресурс уже забронирован на указанное время.")

        return attrs

class QueueEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueEntry
        fields = ['id', 'user', 'booking']
