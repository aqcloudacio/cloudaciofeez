from rest_framework import serializers

from portfolios.models import Portfolio, ModelInvestment
from platforms.models import Platform
from investments.api.serializers import InvestmentNameSerializer
from investments.models import InvestmentName
from users.models import Practice, AFSL


class PortfolioSerializer(serializers.ModelSerializer):
    total_amount = serializers.ReadOnlyField()
    total_inv_fees = serializers.ReadOnlyField()
    total_aa = serializers.ReadOnlyField()
    total_aa_perc = serializers.ReadOnlyField()

    active_practices = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(),
                                                   many=True)

    class Meta:
        model = Portfolio
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PortfolioSerializer, self).__init__(*args, **kwargs)
        platform_id = self.context["platform_id"]
        self.fields['platform'].queryset = Platform.objects.filter(id=platform_id)


class PortfolioTemplateSerializer(serializers.ModelSerializer):

    active_practices = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(),
                                                          many=True,
                                                          required=False)
    afsls = serializers.PrimaryKeyRelatedField(queryset=AFSL.objects.all(),
                                               many=True,
                                               allow_null=True,
                                               required=False)

    class Meta:
        model = Portfolio
        fields = "__all__"


class ModelInvestmentSerializer(serializers.ModelSerializer):

    investment_name = InvestmentNameSerializer(many=False, read_only=True)
    investment_name_id = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentName.objects.all(),
        source='investment_name',
        write_only=True)

    class Meta:
        model = ModelInvestment
        fields = "__all__"
