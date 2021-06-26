from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.forms import FileField, ModelChoiceField, ModelForm

from .models import Album, Image
from .utils import file_utils


class CreateAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'is_public']


class UploadImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['title']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UploadImageForm, self).__init__(*args, **kwargs)
        self.fields['album'] = ModelChoiceField(queryset=Album.objects.filter(owner=user))
        self.fields['file'] = FileField()

    def upload_image(self, file: Union[InMemoryUploadedFile, TemporaryUploadedFile], title: str) -> str:
        """
        Uploads an image file and returns the final location.

        :param file: Django UploadedFile
        :param title: String title of the file provided by the User
        :return: String location of the uploaded file
        """
        upload_location = file_utils.upload_file(file, title)
        return upload_location
