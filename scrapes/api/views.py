from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from scrapes.api.serializers import (InvestmentScrapeSerializer,
                                     InvestmentScrapeSettingsSerializer,
                                     CamelotSettingsSerializer,
                                     PlatformScrapeSettingsSerializer,
                                     AplScrapeSettingsSerializer)

from scrapes.models import (InvestmentScrape, InvestmentScrapeSettings,
                            CamelotSettings, PlatformScrapeSettings,
                            AplScrapeSettings)


class InvestmentScrapeViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = InvestmentScrapeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvestmentScrape.objects.all().order_by("settings")


class InvestmentScrapeSettingsViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = InvestmentScrapeSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvestmentScrapeSettings.objects.all().order_by("platform")


class PlatformScrapeSettingsViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = PlatformScrapeSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlatformScrapeSettings.objects.all().order_by("platform")


class AplScrapeSettingsViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = AplScrapeSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AplScrapeSettings.objects.all().order_by("platform")


class CamelotSettingsViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = CamelotSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CamelotSettings.objects.all().order_by("id")
