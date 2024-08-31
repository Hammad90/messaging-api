from core.models import BaseModel
from user.models import Users
from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    TextChoices,
    DateTimeField,
)

class MemberRole(TextChoices):
    MEMBER = 'member', 'Member'
    ADMIN = 'admin', 'Admin'

class Groups(BaseModel):
    name = CharField(max_length=250)
    created_by = ForeignKey(Users, on_delete=CASCADE)
    description = TextField()
    
    class Meta:
        db_table = "groups"


class GroupMembers(BaseModel):
    group = ForeignKey(Groups, on_delete=CASCADE)
    user = ForeignKey(Users, on_delete=CASCADE)
    role = CharField(max_length=200, choices=MemberRole)
    joined_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "group_members"