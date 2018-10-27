from mongoengine import fields, Document


class Player(Document):
    """This class represents the request model."""
    azurePersonId = fields.StringField(max_length=255)
    name = fields.StringField(max_length=255)
    jerseyNumber = fields.StringField(max_length=255)
    imageUrl = fields.StringField(max_length=255)
    birthday = fields.StringField(max_length=255)
    birthplace = fields.StringField(max_length=255)
    age = fields.StringField(max_length=255)
    height = fields.StringField(max_length=255)
    nationality = fields.StringField(max_length=255)
    position = fields.StringField(max_length=255)
    foot = fields.StringField(max_length=255)
    inTeamSince = fields.StringField(max_length=255)
    contractUntil = fields.StringField(max_length=255)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
