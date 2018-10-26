from mongoengine import fields, Document


class Player(Document):
    """This class represents the request model."""
    id = fields.IntField(primary_key=True)
    name = fields.StringField(max_length=255)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
