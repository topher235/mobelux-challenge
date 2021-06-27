from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from flickrapp.models import Album, Image
from flickrapp.forms import CreateAlbumForm, UploadImageForm


class CreateAlbumFormTest(TestCase):
    def test_fields(self):
        expected_fields = ['name', 'is_public']
        form = CreateAlbumForm()
        self.assertTrue(len(form.fields) == len(expected_fields))
        for field in expected_fields:
            self.assertTrue(field in form.fields)


class UploadImageFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123')
        test_user = User.objects.get(id=1)
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2021', is_public=True,
                             date_created='2021-06-01')

    def test_fields(self):
        expected_fields = ['title', 'album', 'file']
        test_user = User.objects.get(id=1)
        form = UploadImageForm(user=test_user)
        self.assertTrue(len(form.fields) == len(expected_fields))
        for field in expected_fields:
            self.assertTrue(field in form.fields)

    def test_upload_returns_location_from_utility(self):
        expected_location = '/path/to/file.ext'
        test_user = User.objects.get(id=1)
        form = UploadImageForm(user=test_user)
        with patch('flickrapp.forms.file_utils.upload_file', return_value=expected_location):
            actual_location = form.upload_image(None, 'Beach House (front)')
        self.assertEqual(actual_location, expected_location)