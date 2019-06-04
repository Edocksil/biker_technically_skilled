from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    text = models.TextField()
    last_added_text = models.TextField(max_length=140)
    first_added_text_or_name = models.TextField(max_length=140)
    finished = models.BooleanField(default=False)
    contributors = models.ManyToManyField(User)
    count = models.IntegerField(default=0)
    def __str__(self):
        return self.first_added_text_or_name
