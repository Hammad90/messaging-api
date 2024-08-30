from core.models import BaseModel
from django.db.models import CharField, ManyToManyField
from chat.models import Chats

class Users(BaseModel):
    name = CharField(max_length=250)
    phone_number = CharField(max_length=20)
    email = CharField(max_length=100, null=True)
    chats = ManyToManyField(Chats, related_name='user_chats')
    
    class Meta:
        db_table = "users"
