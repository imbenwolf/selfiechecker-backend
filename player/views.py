from rest_framework import viewsets
from .serializers import PlayerSerializer
from .models import Player


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows player to be viewed
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
