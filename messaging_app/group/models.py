from core.models import BaseModel
from user.models import Users
from django.db.models import CharField, ManyToManyField, ForeignKey, CASCADE

class Groups(BaseModel):
    name = CharField(max_length=250)
    created_by = ForeignKey(Users, on_delete=CASCADE)
    users = ManyToManyField(Users, related_name='user_groups')
    
    class Meta:
        db_table = "groups"
