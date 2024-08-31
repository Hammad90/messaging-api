from core.models import BaseModel
from django.db.models import CharField

class Users(BaseModel):
    name = CharField(max_length=250)
    phone_number = CharField(max_length=20)
    email = CharField(max_length=100, null=True)
    
    class Meta:
        db_table = "users"
