from core.models import BaseModel
from user.models import Users
from django.db.models import CharField, ForeignKey, CASCADE

class Chats(BaseModel):
    name = CharField(max_length=200)

    class Meta:
        db_table = "chats"

class UserChat(BaseModel):
    user = ForeignKey(Users, on_delete=CASCADE)
    chat = ForeignKey(Chats, on_delete=CASCADE)

    class Meta:
        db_table = "users_chats"

