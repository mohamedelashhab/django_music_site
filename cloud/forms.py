from django import forms
from django.contrib.auth.models import User
from .models import Album,Song

class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = [
            'title','artist','logo',
        ]

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = [
            'title','audio_file'
        ]

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)
    class Meta:
        model = User
        fields = [
            'first_name','last_name','username','email','password'
        ]