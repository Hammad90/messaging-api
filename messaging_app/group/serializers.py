from rest_framework.serializers import ModelSerializer

from .models import GroupMembers, Groups


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = "__all__"


class GroupMemberSerializer(ModelSerializer):
    class Meta:
        model = GroupMembers
        fields = "__all__"
