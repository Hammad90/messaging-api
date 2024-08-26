from core.models import BaseModel
from user.models import Users
from django.db.models import CharField, ForeignKey, CASCADE

class Groups(BaseModel):
    name = CharField(max_length=250)

    class Meta:
        db_table = "groups"

class UsersGrous(BaseModel):
    user = ForeignKey(Users, on_delete=CASCADE)
    group = ForeignKey(Groups, on_delete=CASCADE)

    class Meta:
        db_table = "users_groups"
