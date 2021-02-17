from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Bathroom(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/

  name = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  description = models.CharField(max_length=100)
  photoUrl = models.URLField(max_length=100)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"Bathroom {self.name} location is '{self.location}', here is the link to bathroom's picture {self.photoUrl}."

  def as_dict(self):
    """Returns dictionary version of Bathroom models"""
    return {
        'id': self.id,
        'name': self.name,
        'location': self.location,
        'description': self.description,
        'photoUrl': self.photoUrl
    }
