from rest_framework import serializers

from flickrapp.models import Album, Image


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'owner', 'name', 'is_public', 'date_created')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'album', 'title', 'location', 'date_uploaded')
