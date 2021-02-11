from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_list_or_404,get_object_or_404

from platforms.models import (Platform, PlatformNames, PlatformFees,
                              PlatformTierThresholds, PlatformTierPercs,
                              PlatformFamilyGroups)
from scenarios.models import Scenario
from portfolios.models import Portfolio
from investments.api.serializers import (AssetAllocationSerializer,
                                         AssetAllocationNameSerializer,
                                         InvestmentSerializer,
                                         InvestmentNameSerializer,
                                         InvestmentClassSerializer)
from investments.models import (AssetAllocation, AssetAllocationName,
                                Investment, InvestmentName, InvestmentClass)


#  Will need to make the platform serializer read-only (except for "name")
#  and make a new serializer to create platform templates.


class PlatformNameSerializer(serializers.ModelSerializer):
    platform_template = serializers.SerializerMethodField()
    linked_investments = serializers.ReadOnlyField()
    PDS_link = serializers.ReadOnlyField()

    class Meta:
        model = PlatformNames
        fields = "__all__"
        extra_fields = ['platforms']

    def get_platform_template(self, obj):
        if obj.platforms.exists():
            try:
                template = get_object_or_404(Platform,
                                          name=obj,
                                          template=True)
                return template.id
            except Exception as e:
                print(e)
        else:
            return None


class PlatformSerializer(serializers.ModelSerializer):

    platform_total = serializers.ReadOnlyField()
    platform_total_fees = serializers.ReadOnlyField()

    str_name = serializers.ReadOnlyField()
    name = PlatformNameSerializer(many=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(
        queryset=PlatformNames.objects.all(), source='name', write_only=True,
        allow_null=True)

    linked_platforms = serializers.ReadOnlyField()
    platform_admin_fee_dollar = serializers.ReadOnlyField()
    platform_admin_fee_percentage_calculated = serializers.ReadOnlyField()
    platform_expense_recovery_dollar = serializers.ReadOnlyField()
    platform_expense_recovery_percentage_calculated = serializers.ReadOnlyField()
    platform_ORR_levy = serializers.ReadOnlyField()
    platform_fund_accounting_fee_dollar = serializers.ReadOnlyField()
    platform_fund_accounting_fee_percentage_calculated = serializers.ReadOnlyField()
    platform_trustee_fee = serializers.ReadOnlyField()
    platform_issuer_fee = serializers.ReadOnlyField()
    platform_sma_admin_fee = serializers.ReadOnlyField()
    switch_fees_total = serializers.ReadOnlyField()
    buy_sell_spread_total = serializers.ReadOnlyField()

    status_list = serializers.SerializerMethodField()
    platform_type_list = serializers.SerializerMethodField()
    allowed_fee_link_list = serializers.SerializerMethodField()
    fee_link_type_list = serializers.SerializerMethodField()


    class Meta:
        model = Platform
        fields = "__all__"
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Platform.objects.all(),
        #         fields=('name', 'template')
        #     )
        # ]

    def __init__(self, *args, **kwargs):
        super(PlatformSerializer, self).__init__(*args, **kwargs)
        if "scenario_id" in self.context:
            scenario_id = self.context["scenario_id"]
            self.fields['scenario'].queryset = Scenario.objects.filter(id=scenario_id)

    def get_status_list(self, obj):
        return Platform.STATUS_CHOICES

    def get_platform_type_list(self, obj):
        return Platform.TYPE_CHOICES

    def get_allowed_fee_link_list(self, obj):
        return Platform.ALLOWED_LINKS

    def get_fee_link_type_list(self, obj):
        return Platform.LINK_TYPES


class PlatformFeeSerializer(serializers.ModelSerializer):
    investment_fee = serializers.ReadOnlyField()
    sliding_admin_fee = serializers.ReadOnlyField()
    platform_fee_total = serializers.ReadOnlyField()
    platform_fee_total_fees = serializers.ReadOnlyField()

    # Calculated properties.
    admin_fee_dollar_calculated = serializers.ReadOnlyField()
    admin_fee_percentage_calculated = serializers.ReadOnlyField()
    ORR_levy_calculated = serializers.ReadOnlyField()
    expense_recovery_percentage_calculated = serializers.ReadOnlyField()
    fund_accounting_fee_percentage_calculated = serializers.ReadOnlyField()
    trustee_fee_calculated = serializers.ReadOnlyField()
    issuer_fee_calculated = serializers.ReadOnlyField()
    low_balance_refund = serializers.ReadOnlyField()

    admin_fee_structure_list = serializers.SerializerMethodField()
    admin_fee_exclusions_list = serializers.SerializerMethodField()

    class Meta:
        model = PlatformFees
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PlatformFeeSerializer, self).__init__(*args, **kwargs)
        platform_id = self.context["platform_id"]
        self.fields['platform'].queryset = Platform.objects.filter(id=platform_id)

    def get_admin_fee_structure_list(self, obj):
        return PlatformFees.STRUCTURE_CHOICES

    def get_admin_fee_exclusions_list(self, obj):
        return PlatformFees.FEE_EXCLUSIONS

class PlatformTierThresholdsSerializer(serializers.ModelSerializer):
    lower_threshold = serializers.ReadOnlyField()

    class Meta:
        model = PlatformTierThresholds
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PlatformTierThresholdsSerializer, self).__init__(*args, **kwargs)
        platformfee_id = self.context["platformfee_id"]
        self.fields['platform_fee_group'].queryset = PlatformFees.objects.filter(id=platformfee_id)


class PlatformTierPercsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformTierPercs
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PlatformTierPercsSerializer, self).__init__(*args, **kwargs)
        platformfee_id = self.context["platformfee_id"]
        self.fields['platform_fee_group'].queryset = PlatformFees.objects.filter(id=platformfee_id)


class PlatformFamilyGroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformFamilyGroups
        fields = "__all__"

############
# Generic helper serializers here
############

class PlatformPortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = "__all__"


    # def __init__(self, *args, **kwargs):
    #     super(PortfolioSerializer, self).__init__(*args, **kwargs)
    #     platform_id = self.context["platform_id"]
    #     platformfee_id = self.context["platformfee_id"]
    #     self.fields['platform'].queryset = Platform.objects.filter(id=platform_id)
    #     self.fields['platform_fee_group'].queryset = PlatformFees.objects.filter(id=platformfee_id)




######################
# Template Serializers here
######################
#
# class PlatformTemplateSerializer(serializers.ModelSerializer):
#     name = PlatformNameSerializer(many=False, read_only=True)
#     name_id = serializers.PrimaryKeyRelatedField(
#         queryset=PlatformNames.objects.all(), source='name', write_only=True)
#
#     class Meta:
#         model = Platform
#         fields = "__all__"
#
#
# class PlatformFeeTemplateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = PlatformFees
#         fields = "__all__"
#
#     def __init__(self, *args, **kwargs):
#         super(PlatformFeeTemplateSerializer, self).__init__(*args, **kwargs)
#         platform_id = self.context["platform_id"]
#         self.fields['platform'].queryset = Platform.objects.filter(id=platform_id)

# class PlatformTierThresholdsTemplateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = PlatformTierThresholds
#         fields = "__all__"
#
#     def __init__(self, *args, **kwargs):
#         super(PlatformTierThresholdsTemplateSerializer, self).__init__(*args, **kwargs)
#         platformfee_id = self.context["platformfee_id"]
#         self.fields['platform_fee_group'].queryset = PlatformFees.objects.filter(id=platformfee_id)
#
#
# class PlatformTierPercsTemplateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = PlatformTierPercs
#         fields = "__all__"
#
#     def __init__(self, *args, **kwargs):
#         super(PlatformTierPercsTemplateSerializer, self).__init__(*args, **kwargs)
#         platformfee_id = self.context["platformfee_id"]
#         self.fields['platform_fee_group'].queryset = PlatformFees.objects.filter(id=platformfee_id)
