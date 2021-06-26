from rest_framework import serializers

from flickrapp.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('owner', 'name', 'is_public', 'date_created')
