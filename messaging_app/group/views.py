from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.models import Users

from .models import GroupMembers, Groups, MemberRole
from .serializers import GroupSerializer


class GroupViewSet(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer

    def create(self, request: Request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "User Id is required to create a group."},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(
                {"error": "User Id does not exist."}, status=HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        GroupMembers.objects.create(
            group=group,
            user=user,
            role=MemberRole.ADMIN,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class JoinGroupAPIView(APIView):
    def post(self, request: Request):
        user_id = request.data.get("user_id")
        group_id = request.data.get("group_id")

        if not user_id or not group_id:
            return Response(
                {"error": "User Id and Group Id are required."},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            user = Users.objects.get(id=user_id)
            group = Groups.objects.get(id=group_id)
        except Users.DoesNotExist:
            return Response(
                {"error": "User Id does not exist"}, status=HTTP_404_NOT_FOUND
            )
        except Groups.DoesNotExist:
            return Response(
                {"error": "Group does not exist"}, status=HTTP_404_NOT_FOUND
            )
        if GroupMembers.objects.filter(user=user, group=group).exists():
            return Response(
                {"error": "User is already a member of the group"},
                status=HTTP_400_BAD_REQUEST,
            )
        if GroupMembers.objects.filter(
            user=user, group=group, role=MemberRole.ADMIN
        ).exists():
            return Response(
                {"error": "Group admin cannot request to join the group"},
                status=HTTP_400_BAD_REQUEST,
            )
        GroupMembers.objects.create(user=user, group=group, role=MemberRole.MEMBER)
        return Response({"status": "User has joined the group"}, status=HTTP_200_OK)


class LeaveGroupAPIView(APIView):
    def post(self, request: Request):
        user_id = request.data.get("user_id")
        group_id = request.data.get("group_id")
        if not user_id or not group_id:
            return Response(
                {"error": "User Id and Group Id are required."},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            user = Users.objects.get(id=user_id)
            group = Groups.objects.get(id=group_id)
        except Users.DoesNotExist:
            return Response(
                {"error": "User Id does not exist"}, status=HTTP_404_NOT_FOUND
            )
        except Groups.DoesNotExist:
            return Response(
                {"error": "Group does not exist"}, status=HTTP_404_NOT_FOUND
            )

        group_member = GroupMembers.objects.filter(user=user, group=group).first()
        if not group_member:
            return Response(
                {"error": "User is not a member of the group."},
                status=HTTP_400_BAD_REQUEST,
            )

        if group_member.role == MemberRole.ADMIN:
            return Response(
                {"error": "Group admin cannot leave the group"},
                status=HTTP_400_BAD_REQUEST,
            )
        group_member.delete()
        return Response(
            {"status": f"{user.name} has left the group"}, status=HTTP_200_OK
        )
