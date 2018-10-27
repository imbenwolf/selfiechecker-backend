from rest_framework_mongoengine import routers
from django.urls import path
from .views import PlayerViewSet, UpdatePlayerView

router = routers.DefaultRouter()
router.register(r'', PlayerViewSet)

urlpatterns = [
    path('update/', UpdatePlayerView.as_view()),
]

urlpatterns += router.urls
