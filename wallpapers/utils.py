from .models import Booking, QueueEntry
from datetime import timedelta

def is_slot_available(resource, start_time):
    bookings = Booking.objects.filter(
        resource=resource,
        start_time__lt=start_time + timedelta(minutes=resource.slot_duration),
        end_time__gt=start_time
    )
    return bookings.count() < resource.max_capacity

def add_to_queue(user, resource):
    QueueEntry.objects.create(user=user)

def release_slot(booking):
    next_in_queue = Booking.objects.filter(booking=None).first()
    if next_in_queue:
        # Создаем новое бронирование для следующего в очереди
        new_booking = Booking.objects.create(
            user=next_in_queue.user,
            resource=booking.resource,
            start_time=booking.start_time,  # Используем время, которое освободилось
            end_time=booking.end_time,
            status='active'
        )

        # Обновляем запись в очереди
        next_in_queue.booking = new_booking
        next_in_queue.save()


        print(f"Уведомление: {next_in_queue.user} ваш слот был забронирован.")