from rest_framework import serializers

from flickrapp.models import Album, Image


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('owner', 'name', 'is_public', 'date_created')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('album', 'title', 'location', 'date_uploaded')
