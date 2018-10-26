from django.db import models


class Player(models.Model):
    """This class represents the request model."""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
