from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Album, Image
from .forms import CreateAlbumForm, UploadImageForm


class AlbumModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123')
        test_user = User.objects.get(id=1)
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2021', is_public=True, date_created='2021-06-01')
        Album.objects.create(owner=test_user, name='Ski mountain 2021', is_public=False, date_created='2021-01-01')

    def test_album_name_label(self):
        album = Album.objects.get(id=1)
        field_label = album._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Album name')

    def test_is_public_label(self):
        album = Album.objects.get(id=1)
        field_label = album._meta.get_field('is_public').verbose_name
        self.assertEqual(field_label, 'Public?')

    def test_name_max_length(self):
        album = Album.objects.get(id=1)
        field_max_length = album._meta.get_field('name').max_length
        self.assertEqual(field_max_length, 80)

    def test_ordering(self):
        album = Album.objects.get(id=1)
        field_ordering = album._meta.ordering
        self.assertEqual(len(field_ordering), 1)
        self.assertEqual(field_ordering[0], 'date_created')


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123')
        test_user = User.objects.get(id=1)
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2021', is_public=True,
                             date_created='2021-06-01')
        album = Album.objects.get(id=1)
        Image.objects.create(album=album, title='Beach house (front)', location='filename.ext',
                             date_uploaded='2021-06-02')

    def test_title_label(self):
        image = Image.objects.get(id=1)
        field_label = image._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Photo title')

    def test_title_max_length(self):
        album = Image.objects.get(id=1)
        field_max_length = album._meta.get_field('title').max_length
        self.assertEqual(field_max_length, 80)

    def test_location_max_length(self):
        album = Image.objects.get(id=1)
        field_max_length = album._meta.get_field('location').max_length
        self.assertEqual(field_max_length, 120)

    def test_ordering(self):
        image = Image.objects.get(id=1)
        field_ordering = image._meta.ordering
        self.assertEqual(len(field_ordering), 1)
        self.assertEqual(field_ordering[0], 'date_uploaded')


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
