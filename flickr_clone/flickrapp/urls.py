from django.urls import path

from .views import CreateAlbumView, AlbumListForUserView, UploadImageView


urlpatterns = [
    path('create-album/', CreateAlbumView.as_view(), name='create_album'),
    path('albums/<username>', AlbumListForUserView.as_view(), name='user_albums'),
    path('upload-image', UploadImageView.as_view(), name='upload_image'),
]
