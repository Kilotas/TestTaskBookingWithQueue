from django.contrib import admin
from .models import QueueEntry, Queue, Resource, Booking
# Register your models here.

admin.site.register(QueueEntry)
admin.site.register(Queue)
admin.site.register(Resource)
admin.site.register(Booking)




