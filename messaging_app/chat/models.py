from core.models import BaseModel
from django.db.models import ManyToManyField
from user.models import Users

class Chats(BaseModel):
    members = ManyToManyField(Users)
    
    class Meta:
        db_table = "chats"
