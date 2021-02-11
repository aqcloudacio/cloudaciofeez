from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import date

from adverts.api.serializers import (AdvertSerializer, AdvertTypeSerializer,
                                     AdvertiserSerializer)
from adverts.models import Advert, AdvertType, Advertiser



#### Viewsets

class CurrentAdvertViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = date.today()
        return Advert.objects.filter(start_date__lte=today,
                                     end_date__gte=today
                                     ).order_by("name")


class AdvertViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]
    queryset = Advert.objects.all().order_by("name")


class AdvertTypeViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AdvertTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = AdvertType.objects.all().order_by("type")


class AdvertiserViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = AdvertiserSerializer
    permission_classes = [IsAuthenticated]
    queryset = Advertiser.objects.all().order_by("name")
