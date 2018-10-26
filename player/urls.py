from rest_framework_mongoengine import routers
from .views import PlayerViewSet

router = routers.DefaultRouter()
router.register(r'', PlayerViewSet)

urlpatterns = router.urls
