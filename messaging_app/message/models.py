from core.models import BaseModel
from user.models import Users
from group.models import Groups
from chat.models import Chats
from django.db.models import (
    CharField,
    ForeignKey,
    CASCADE,
    TextChoices,
    TextField,
    DateTimeField
)

class MessageType(TextChoices):
    TEXT = 'text', 'Text'
    IMAGE = 'image', 'Image'
    VIDEO = 'video', 'Video'
    FILE = 'file', 'File'

class Messages(BaseModel):
    user = ForeignKey(Users, on_delete=CASCADE)
    group = ForeignKey(Groups, on_delete=CASCADE, null=True, blank=True)
    chat = ForeignKey(Chats, on_delete=CASCADE, null=True, blank=True)
    message_type = CharField(max_length=100, choices=MessageType.choices)
    content = TextField()
    sent_at = DateTimeField(auto_now_add=True)
    delivered_at = DateTimeField(null=True, blank=True)
    seen_at = DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "messages"
