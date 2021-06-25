from django.forms import ModelForm, RadioSelect

from .models import Album


class CreateAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'is_public']
