from django.urls import include, path
from rest_framework import routers

from .views import AlbumViewSet


router = routers.DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='Album')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
