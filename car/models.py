from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    text = models.TextField()
    last_added_text = models.TextField()
    first_added_text_or_name = models.TextField()
    finished = models.BooleanField()
    contributors = models.ManyToManyField(User)

    def str(self):
        return self.first_added_text_or_name
