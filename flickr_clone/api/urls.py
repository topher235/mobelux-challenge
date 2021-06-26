from django.urls import include, path
from rest_framework import routers

from .views import AlbumViewSet, ImageViewSet


router = routers.DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='Album')
router.register(r'images', ImageViewSet, basename='Image')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
