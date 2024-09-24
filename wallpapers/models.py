from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    name = models.CharField(max_length=100)  #
    slot_duration = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(240)]
            )
    max_duration = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(480)]
    )
    max_capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.name} (Слот: {self.slot_duration} мин, Максимальная длительность: {self.max_duration} мин, Вместимость: {self.max_capacity})"


# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активное'),
        ('queued', 'В очереди'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='queued')
    created_at = models.DateTimeField(auto_now_add=True)  # Исправлено
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return f'Booking for {self.resource} by {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.start_time + timedelta(minutes=self.resource.slot_duration)
        return super().save(*args, **kwargs)

class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    queue_position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['queue_position']  # Automatically order by queue position

    def str(self):
        return f'Queue position {self.queue_position} for {self.resource} by {self.user.username}'

class QueueEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Queue entry for {self.user.username}'


