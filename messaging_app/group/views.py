from rest_framework.viewsets import ModelViewSet
from .models import Groups
from .serializers import GroupSerializer

class GroupViewSet(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
