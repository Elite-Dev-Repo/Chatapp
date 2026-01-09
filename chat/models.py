from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_messages')


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
