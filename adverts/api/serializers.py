from rest_framework import serializers
from adverts.models import AdvertType, Advertiser, Advert
from portfolios.models import Portfolio

##################
# Helper/Shortcut serializers
#################


class AdvertTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvertType
        fields = "__all__"


class AdvertiserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertiser
        fields = "__all__"


class AdvertSerializer(serializers.ModelSerializer):

    type_name = serializers.SerializerMethodField()
    platform_name = serializers.ReadOnlyField()
    investment_name = serializers.ReadOnlyField()

    class Meta:
        model = Advert
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdvertSerializer, self).__init__(*args, **kwargs)
        self.fields['portfolio_template'].queryset = Portfolio.objects.filter(template=True)


    def get_type_name(self, instance):
        return instance.type.type
