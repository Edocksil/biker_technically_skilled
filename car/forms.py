from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['last_added_text']

class StoryAddForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['last_added_text', 'finished']
