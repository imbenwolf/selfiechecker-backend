from rest_framework_mongoengine import viewsets
from rest_framework.views import APIView
from .serializers import PlayerSerializer
from .models import Player
from rest_framework.response import Response
from .utils.player_crawler import PlayerInfos


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows player to be viewed
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class UpdatePlayerView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    @staticmethod
    def get(request, format=None):
        result = {
            "updated": True
        }

        players = PlayerInfos.get_player_infos()
        for player in players:
            player_serializer = PlayerSerializer(data=player)
            if player_serializer.is_valid():
                player_serializer.save()
            else:
                result["updated"] = False
                result["errors"] = player_serializer.errors

                return Response(result)
        return Response(result)
