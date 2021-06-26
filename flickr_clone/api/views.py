from rest_framework import viewsets

from .serializers import AlbumSerializer, ImageSerializer
from flickrapp.models import Album, Image


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filterset_fields = ['owner']


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_fields = ['album']
