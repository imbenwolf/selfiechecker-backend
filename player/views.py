from rest_framework_mongoengine import viewsets
from .serializers import PlayerSerializer
from .models import Player


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows player to be viewed
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
