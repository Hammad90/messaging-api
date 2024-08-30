from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from .models import Groups
from user.models import Users
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from .serializers import GroupSerializer


class GroupViewSet(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=['post'])
    def join_group(self, request: Request, pk=None):
        user_id: str = request.data.get('userID')
        group = self.get_object()
        user = Users.objects.get(id=user_id)
        group.users.add(user)
        return Response(
            {'status': 'user joined group'},
            status=HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def leave_group(self, request: Request, pk=None):
        user_id: str = request.data.get('userID')
        group = self.get_object()
        user = Users.objects.get(id=user_id)
        group.members.remove(user)
        return Response(
            {'status': 'user left group'},
            status=HTTP_200_OK
        )
