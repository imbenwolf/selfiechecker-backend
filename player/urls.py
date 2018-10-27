from django.urls import path
from .views import PlayerView, UpdatePlayerView

urlpatterns = [
    path('', PlayerView.as_view()),
    path('update/', UpdatePlayerView.as_view()),
]
