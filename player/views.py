from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from .serializers import PlayerSerializer
from .models import Player
from rest_framework.response import Response
from .utils.player_crawler import PlayerCrawler
from .utils.player_identifier import PlayerIdentifier


class PlayerView(APIView):
    """
    API endpoint that allows players to be viewed and a player to be detected by a selfie
    """
    parser_classes = (FileUploadParser,)

    @staticmethod
    def get(format=None):
        players = Player.objects.all()
        player_serializer = PlayerSerializer(players, many=True)
        return Response(player_serializer.data)

    @staticmethod
    def put(request, format=None):
        file = request.data['file']
        player_name = PlayerIdentifier.get_person_from_image(file)[0]
        player = Player.objects.filter(name=player_name)[0]
        player_serializer = PlayerSerializer(player)
        return Response(player_serializer.data)


class UpdatePlayerView(APIView):
    """
    API endpoint that updates the information of the players aswell as setup and train the image recognition ai
    """
    @staticmethod
    def get(request, format=None):
        result = {
            "updated": True
        }

        people = []
        players = PlayerCrawler.get_player_infos()
        for player in players:
            player_serializer = PlayerSerializer(data=player)
            if player_serializer.is_valid():
                player_serializer.save()
                people.append({
                    'name': player['name'],
                    'faces': [
                        {
                            'url': player['imageUrl']
                        }
                    ]
                })
            else:
                result["updated"] = False
                result["errors"] = player_serializer.errors

                return Response(result)

        PlayerIdentifier.create_and_train_person_group(people)
        return Response(result)
