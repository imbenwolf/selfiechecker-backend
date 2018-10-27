from rest_framework_mongoengine import serializers
from .models import Player


class PlayerSerializer(serializers.DocumentSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Player
        fields = (
            'id',
            'name',
            'jerseyNumber',
            'imageUrl',
            'birthday',
            'birthplace',
            'age',
            'height',
            'nationality',
            'position',
            'foot',
        )
