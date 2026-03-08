from django import forms
from .models import Movie, Creator


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ('title','year','description','poster')


class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields ='__all__'