from core.models import BaseModel
from django.db.models import CharField

class Chats(BaseModel):
    name = CharField(max_length=200)

    class Meta:
        db_table = "chats"
