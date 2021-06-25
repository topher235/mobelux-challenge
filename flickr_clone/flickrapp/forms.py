from django.forms import ModelForm

from .models import Album


class CreateAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'is_public']
