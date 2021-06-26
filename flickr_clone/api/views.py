from rest_framework import viewsets

from .serializers import AlbumSerializer
from flickrapp.models import Album


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filterset_fields = ['owner']
