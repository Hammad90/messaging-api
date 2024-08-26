from rest_framework.serializers import ModelSerializer
from .models import Groups

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id', 'name', 'created_at', 'updated_at']
