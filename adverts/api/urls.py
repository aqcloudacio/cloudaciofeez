from django.urls import include, path
from rest_framework.routers import SimpleRouter

from adverts.api import views

app_name = "adverts"

#########
# Routes
#########
router = SimpleRouter()
router.register(r"currentadvert", views.CurrentAdvertViewSet, "currentadvert")
router.register(r"advert", views.AdvertViewSet)
router.register(r"adverttype", views.AdvertTypeViewSet)
router.register(r"advertiser", views.AdvertiserViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
