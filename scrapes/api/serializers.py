from rest_framework import serializers

from scrapes.models import (InvestmentScrape, InvestmentScrapeSettings,
                            CamelotSettings, PlatformScrapeSettings,
                            AplScrapeSettings)

class InvestmentScrapeSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()

    class Meta:
        model = InvestmentScrape
        fields = "__all__"

    def get_full_name(self, instance):
        if instance.name:
            return str(instance.name)
        else:
            return ''

    def get_platform(self, instance):
        if instance.name:
            return str(instance.name.platform)
        else:
            return ''


class InvestmentScrapeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentScrapeSettings
        fields = "__all__"


class PlatformScrapeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformScrapeSettings
        fields = "__all__"


class AplScrapeSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AplScrapeSettings
        fields = "__all__"


class CamelotSettingsSerializer(serializers.ModelSerializer):

    platform = serializers.ReadOnlyField()

    class Meta:
        model = CamelotSettings
        fields = "__all__"
