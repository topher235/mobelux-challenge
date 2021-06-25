from django.urls import path

from .views import CreateAlbumView


urlpatterns = [
    path('create-album/', CreateAlbumView.as_view(), name='create_album'),
]
