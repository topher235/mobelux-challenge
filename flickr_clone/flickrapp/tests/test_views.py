from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from flickrapp.models import Album, Image


class CreateAlbumViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create_album'))
        self.assertRedirects(response, '/accounts/login/?next=/flickr/create-album/')

    def test_logged_in_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/flickr/create-album/')
        # Check that the user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_album'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_album'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/create-album.html')

    def test_redirects_to_profile_on_success(self):
        user = User.objects.get(id=1)
        self.client.login(username=user.username, password='testpassword')
        form_data = {
            'owner': user,
            'name': 'Beach Vacation 2021',
            'is_public': True
        }
        response = self.client.post(reverse('create_album'), data=form_data)
        self.assertRedirects(response, reverse('profile'))

    def test_album_saves(self):
        user = User.objects.get(id=1)
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'owner': user,
            'name': 'Beach Vacation 2022',
            'is_public': False
        }
        self.client.post(reverse('create_album'), data=form_data)
        # Get album from db
        album = Album.objects.get(id=1)
        self.assertEqual(album.owner, form_data['owner'])
        self.assertEqual(album.name, form_data['name'])
        self.assertEqual(album.is_public, form_data['is_public'])


class AlbumListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123')
        test_user = User.objects.get(id=1)
        # 10 albums
        # test_user has 10 albums -- 5 private, 5 public
        for i in range(1, 11):
            is_public = i % 2 == 0
            Album.objects.create(owner=test_user, name=f'Album {i}', is_public=is_public,
                                 date_created=f'2021-01-{str(i).zfill(2)}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/flickr/albums/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('album_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albums/list-all-albums.html')

    def test_lists_only_public_albums(self):
        public_albums = Album.objects.filter(is_public=True)
        response = self.client.get(reverse('album_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['album_list']), len(public_albums))


class AlbumListForUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123', password='testUser123pass')
        User.objects.create_user(username='testUser789', password='testUser789pass')
        test_user = User.objects.get(id=1)
        test_user2 = User.objects.get(id=2)
        # 10 albums
        # test_user has 2 albums -- 1 private, 1 public
        # test_user2 has 8 albums -- 4 private, 4 public
        for i in range(1, 11):
            is_public = i % 2 == 0
            owner = test_user if i % 5 == 0 else test_user2
            Album.objects.create(owner=owner, name=f'Album {i}', is_public=is_public,
                                 date_created=f'2021-01-{str(i).zfill(2)}')

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user_albums', kwargs={'username': 'testUser123'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albums/list-albums.html')

    def test_logged_in_requesting_own_albums(self):
        self.client.login(username='testUser123', password='testUser123pass')
        response = self.client.get(reverse('user_albums', kwargs={'username': 'testUser123'}))
        # testUser123 has 2 albums -- 1 private, 1 public
        self.assertEqual(len(response.context['album_list']), 2)
        num_public = len([a for a in response.context['album_list'] if a.is_public])
        num_private = len([a for a in response.context['album_list'] if not a.is_public])
        self.assertEqual(num_public, 1)
        self.assertEqual(num_private, 1)

    def test_logged_in_requesting_another_user_albums(self):
        self.client.login(username='testUser123', password='testUser123pass')
        response = self.client.get(reverse('user_albums', kwargs={'username': 'testUser789'}))
        # testUser789 has 8 albums -- 4 private, 4 public
        # testUser123 should only see 4 public albums
        self.assertEqual(len(response.context['album_list']), 4)
        num_public = len([a for a in response.context['album_list'] if a.is_public])
        num_private = len([a for a in response.context['album_list'] if not a.is_public])
        self.assertEqual(num_public, 4)
        self.assertEqual(num_private, 0)

    def test_not_logged_in_requesting_user_albums(self):
        response = self.client.get(reverse('user_albums', kwargs={'username': 'testUser789'}))
        # testUser789 has 8 albums -- 4 private, 4 public
        # anonymous user should only see 4 public albums
        self.assertEqual(len(response.context['album_list']), 4)
        num_public = len([a for a in response.context['album_list'] if a.is_public])
        num_private = len([a for a in response.context['album_list'] if not a.is_public])
        self.assertEqual(num_public, 4)
        self.assertEqual(num_private, 0)

    def test_username_provided_to_context(self):
        self.client.login(username='testUser123', password='testUser123pass')
        response = self.client.get(reverse('user_albums', kwargs={'username': 'testUser123'}))
        self.assertTrue('username' in response.context)
        self.assertEqual(response.context['username'], 'testUser123')

    def test_requested_username_not_exists_returns_status_code_404(self):
        response = self.client.get(reverse('user_albums', kwargs={'username': 'nonexistentUser'}))
        self.assertEqual(response.status_code, 404)


class ImageListForAlbumViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testUser123')
        test_user = User.objects.get(id=1)
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2021', is_public=True,
                             date_created='2021-06-01')
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2022', is_public=False,
                             date_created='2022-06-01')
        album = Album.objects.get(id=1)
        album2 = Album.objects.get(id=2)
        Image.objects.create(album=album, title='Beach house (front)', location='filename.ext',
                             date_uploaded='2021-06-02')
        Image.objects.create(album=album2, title='Ice cream', location='file2.ext', date_uploaded='2022-06-02')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/flickr/albums/1/images')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('image_list', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('image_list', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albums/list-images.html')

    def test_requested_album_not_exists_returns_status_code_404(self):
        response = self.client.get(reverse('image_list', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_requested_album_is_private_returns_status_code_403(self):
        response = self.client.get(reverse('image_list', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 403)

    def test_view_returns_images_for_public_album(self):
        response = self.client.get(reverse('image_list', kwargs={'pk': 1}))
        self.assertEqual(len(response.context['image_list']), 1)

    def test_album_provided_to_context(self):
        album = Album.objects.get(id=1)
        response = self.client.get(reverse('image_list', kwargs={'pk': 1}))
        self.assertTrue('album' in response.context)
        self.assertEqual(response.context['album'], album)


class UploadImageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='testpassword')
        test_user = User.objects.get(id=1)
        Album.objects.create(owner=test_user, name='Beach Vacation Summer 2021', is_public=True,
                             date_created='2021-06-01')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('upload_image'))
        self.assertRedirects(response, '/accounts/login/?next=/flickr/upload-image/')

    def test_logged_in_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/flickr/upload-image/')
        # Check that the user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('upload_image'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('upload_image'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/upload-image.html')

    def test_redirects_to_profile_on_success(self):
        # login
        self.client.login(username='testuser', password='testpassword')
        album = Album.objects.get(id=1)
        with open('./test_data/file.txt', 'r') as file:
            form_data = {
                'album': album.id,  # have to use id for ModelChoiceField, cannot use the album object
                'title': 'Temporary file',
                'file': file
            }
            # mock out the actual file upload function
            with patch('flickrapp.forms.UploadImageForm.upload_image', return_value='file_location.ext'):
                response = self.client.post(reverse('upload_image'), data=form_data)
                self.assertRedirects(response, reverse('profile'))

    def test_image_model_saves(self):
        # login
        self.client.login(username='testuser', password='testpassword')
        album = Album.objects.get(id=1)
        with open('./test_data/file.txt', 'r') as file:
            form_data = {
                'album': album.id,  # have to use id for ModelChoiceField, cannot use the album object
                'title': 'Temporary file',
                'file': file
            }
            # mock out the actual file upload function
            with patch('flickrapp.forms.UploadImageForm.upload_image', return_value='file_location.ext'):
                self.client.post(reverse('upload_image'), data=form_data)
            # Assert image model saved
            image = Image.objects.get(id=1)
            self.assertEqual(image.album.id, form_data['album'])
            self.assertEqual(image.title, form_data['title'])
            self.assertEqual(image.location, 'file_location.ext')