from core.models import BaseModel
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    TextChoices,
    TextField,
)
from user.models import Users


class MemberRole(TextChoices):
    MEMBER = "member", "Member"
    ADMIN = "admin", "Admin"


class Groups(BaseModel):
    name = CharField(max_length=250)
    created_by = ForeignKey(Users, on_delete=CASCADE, related_name="created_by")
    description = TextField(blank=True)

    class Meta:
        db_table = "groups"


class GroupMembers(BaseModel):
    group = ForeignKey(Groups, on_delete=CASCADE)
    user = ForeignKey(Users, on_delete=CASCADE)
    role = CharField(max_length=200, choices=MemberRole)
    joined_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "group_members"
