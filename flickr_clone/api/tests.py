from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from flickrapp.models import Album, Image


class AlbumTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123')
        User.objects.create_user(username='testUser789')
        test_user = User.objects.get(id=1)
        test_user2 = User.objects.get(id=2)
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2021', is_public=True,
                             date_created='2021-06-01')
        Album.objects.create(owner=test_user, name='Ski mountain 2021', is_public=False, date_created='2021-01-01')
        Album.objects.create(owner=test_user2, name='Labrador', is_public=True, date_created='2022-01-01')

    def test_get_all_albums(self):
        url = '/api/v1/albums/'
        owner1 = User.objects.get(id=1)
        owner2 = User.objects.get(id=2)
        # Albums are sorted by date_created
        expected_data = [
            {
                'id': 2,
                'owner': owner1.id,
                'name': 'Ski mountain 2021',
                'is_public': False,
                'date_created': '2021-01-01'
            },
            {
                'id': 1,
                'owner': owner1.id,
                'name': 'Beach Vacation Summer 2021',
                'is_public': True,
                'date_created': '2021-06-01'
            },
            {
                'id': 3,
                'owner': owner2.id,
                'name': 'Labrador',
                'is_public': True,
                'date_created': '2022-01-01'
            }
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_albums_for_user(self):
        owner = User.objects.get(id=1)
        url = f'/api/v1/albums/?owner={owner.id}'
        expected_data = [
            {
                'id': 2,
                'owner': owner.id,
                'name': 'Ski mountain 2021',
                'is_public': False,
                'date_created': '2021-01-01'
            },
            {
                'id': 1,
                'owner': owner.id,
                'name': 'Beach Vacation Summer 2021',
                'is_public': True,
                'date_created': '2021-06-01'
            },
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class ImageTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123')
        test_user = User.objects.get(id=1)
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2021', is_public=True,
                             date_created='2021-06-01')
        album = Album.objects.get(id=1)
        Image.objects.create(album=album, title='Beach House (front)', location='file.txt', date_uploaded='2021-06-02')

    def test_get_images(self):
        url = '/api/v1/images/'
        album = Album.objects.get(id=1)
        # Images are sorted by date_uploaded
        expected_data = [
            {
                'id': 1,
                'album': album.id,
                'title': 'Beach House (front)',
                'location': 'file.txt',
                'date_uploaded': '2021-06-02'
            },
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_image_for_album(self):
        album = Album.objects.get(id=1)
        url = f'/api/v1/images/?album={album.id}'
        # Images are sorted by date_uploaded
        expected_data = [
            {
                'id': 1,
                'album': album.id,
                'title': 'Beach House (front)',
                'location': 'file.txt',
                'date_uploaded': '2021-06-02'
            },
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
