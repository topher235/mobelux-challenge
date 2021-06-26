from django.shortcuts import redirect
from django.urls import path

from .views import CreateAlbumView, AlbumListView, AlbumListForUserView, ImageListForAlbumView, UploadImageView


urlpatterns = [
    path('', lambda request: redirect('albums/', permanent=True)),
    path('create-album/', CreateAlbumView.as_view(), name='create_album'),
    path('upload-image/', UploadImageView.as_view(), name='upload_image'),
    path('albums/', AlbumListView.as_view(), name='album_list'),
    path('albums/<pk>/images', ImageListForAlbumView.as_view(), name='image_list'),
    path('<username>/albums', AlbumListForUserView.as_view(), name='user_albums'),
]
