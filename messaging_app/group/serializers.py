from rest_framework.serializers import ModelSerializer
from .models import Groups, GroupMembers

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'

class GroupMemberSerializer(ModelSerializer):
    class Meta:
        model = GroupMembers
        fields = '__all__'