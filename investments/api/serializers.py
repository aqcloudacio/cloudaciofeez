from rest_framework import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from investments.models import (Investment, InvestmentClass, AssetAllocation,
                                AssetAllocationName, InvestmentName,
                                NABInvestment)
from portfolios.models import Portfolio
from platforms.models import PlatformFees
from riskprofiles.models import RiskProfileAAName
from rest_framework.fields import CurrentUserDefault


##################
# Helper/Shortcut serializers
#################

class AssetAllocationSimpleSerializer(serializers.ModelSerializer):
    '''
    Just used for the investment serializers so I can bulk save asset allocation
    and avoid multiple API calls.

    '''
    class Meta:
        model = AssetAllocation
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': False}}

#############
# Main serializers
#############

class InvestmentNameSerializer(serializers.ModelSerializer):
    linked_inv = serializers.ReadOnlyField()
    extended_name = serializers.ReadOnlyField()
    investment_class = serializers.ReadOnlyField()

    class Meta:
        model = InvestmentName
        fields = "__all__"


class InvestmentClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentClass
        fields = "__all__"


class InvestmentSerializer(serializers.ModelSerializer):
    investment_fee_dollar = serializers.ReadOnlyField()
    investment_fee = serializers.ReadOnlyField()

    name = InvestmentNameSerializer(many=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentName.objects.all(), source='name', write_only=True,
        allow_null=True)

    investment_class = InvestmentClassSerializer(many=False, read_only=True)
    investment_class_id = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentClass.objects.all(),
        source='investment_class',
        write_only=True, allow_null=True)

    platform_fee_group_name = serializers.SerializerMethodField()

    status = serializers.ReadOnlyField()
    transaction = serializers.ReadOnlyField()

    asset_allocations = AssetAllocationSimpleSerializer(many=True, required=False)

    class Meta:
        model = Investment
        fields = "__all__"
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Investment.objects.all(),
        #         fields=('name', 'template')
        #     )
        # ]

    def __init__(self, *args, **kwargs):
        super(InvestmentSerializer, self).__init__(*args, **kwargs)
        if "portfolio_id" in self.context:
            portfolio_id = self.context["portfolio_id"]
            self.fields['portfolio'].queryset = Portfolio.objects.filter(id=portfolio_id)

    def update(self, instance, validated_data):
        '''
        Modified to allow bulk creation/deletion/updating of asset allocation
        '''
        print(validated_data)
        if 'asset_allocations' in validated_data:
            aa_data = validated_data.pop('asset_allocations')
            print(aa_data)
            clear_aa = validated_data['clear_aa']
            validated_data['clear_aa'] = False
            investment = super().update(instance, validated_data)

            if clear_aa:
                # If the aa needs to be cleared and reset with standard fields
                # i.e. if asset allocation from scrapes is being edited.
                instance.asset_allocations.all().delete()
                for aa in aa_data:
                    print(aa)
                    new_aa_instance = AssetAllocation(investment=instance,
                                                      rp_name_id=aa['rp_name_id'],
                                                      percentage=aa['percentage'])
                    new_aa_instance.save()
            else:
                # If the existing aa needs updating or new aa items need adding:
                for aa in aa_data:
                    if aa.get('id',False):
                        # updating existing items
                        existing_instance = get_object_or_404(AssetAllocation,
                                                               id=aa['id'])

                        if aa['percentage'] != existing_instance.percentage:
                            print(f"{aa['name']} has changed")
                            #If the aa item has changed
                            existing_instance.percentage = aa['percentage']
                            existing_instance.save()
                        else:
                            print(f"{aa['name']} has not changed")
                    else:
                        # New AA items
                        print(f"{aa['rp_name_id']} is a new item")
                        new_aa_instance = AssetAllocation(investment=instance,
                                                          rp_name_id=aa['rp_name_id'],
                                                          percentage=aa['percentage'])
                        new_aa_instance.save()

        else:
            investment = super().update(instance, validated_data)

        return investment


    def get_platform_fee_group_name(self, instance):
        if instance.platform_fee_group:
            try:
                fee_group = get_object_or_404(PlatformFees, id=instance.platform_fee_group.id)
                return fee_group.description
            except Exception as e:
                print(e)
        else:
            return None


class AssetAllocationNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetAllocationName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AssetAllocationNameSerializer, self).__init__(*args, **kwargs)
        self.fields['rp_aaname_link'].child_relation.queryset = RiskProfileAAName.objects.filter(template=True, group__default=True)


class AssetAllocationSerializer(serializers.ModelSerializer):
    name = AssetAllocationNameSerializer(many=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetAllocationName.objects.all(), source='name',
        write_only=True, allow_null=True)
    aa_dollar = serializers.ReadOnlyField()
    rp_aa_custom_name = serializers.SerializerMethodField()
    rp_aa_percentage = serializers.SerializerMethodField()
    rp_aa_dollar = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()

    class Meta:
        model = AssetAllocation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AssetAllocationSerializer, self).__init__(*args, **kwargs)
        if "investment_id" in self.context:
            investment_id = self.context["investment_id"]
            self.fields['investment'].queryset = Investment.objects.filter(id=investment_id)

    def get_platform(self, instance):
        if self.context.get("platform_id"):
            return int(self.context.get("platform_id"))
        else:
            return None

    def get_rp_aa_custom_name(self, obj):
        '''
        Matches the "rp_aaname_link" of an asset allocation to the templated
        asset allocation name. Then matches this templated name to the user's
        instance of asset allocation names and retrieves the customised name.

        There will always be a customised name as it is set to the default name
        on instantiation. The "name" can not be changed and should not be
        editable via the API.

        Will only retrieve the risk profile names that are linked to the
        "active" risk profile group.
        '''
        try:
            user = self.context["request"].user
            rp_aaname_links = list(obj.name.rp_aaname_link.all())
            user_aa_names = get_list_or_404(RiskProfileAAName,
                                            group__allowed_users__in=[user],
                                            name__in=rp_aaname_links,
                                            group__active_users__in=[user])
            name_list = []
            for aa_name in user_aa_names:
                name_list.append(aa_name.custom_name)
            return name_list
        except Exception as e:
            print(e)

    def get_rp_aa_percentage(self, obj):
        '''
        If the asset allocation is linked to more than one templated aa name,
        this field will evenly split the actual asset allocation dollar amount
        across the number of linked aa names.
        '''
        if obj.name:
            number_of_links = len(obj.name.rp_aaname_link.all())
            if not number_of_links:
                # In case the aaname is not yet assigned to an rpaaname
                number_of_links = 1
            return (obj.percentage/number_of_links)
        else:
            return None

    def get_rp_aa_dollar(self, obj):
        '''
        If the asset allocation is linked to more than one templated aa name,
        this field will evenly split the actual asset allocation percentage
        across the number of linked aa names.
        '''
        if obj.name:
            number_of_links = len(obj.name.rp_aaname_link.all())
            if not number_of_links:
                # In case the aaname is not yet assigned to an rpaaname
                number_of_links = 1
            return (obj.aa_dollar/number_of_links)
        else:
            return None

class NABInvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = NABInvestment
        fields = "__all__"

##################
# Template serializers
#################

class InvestmentTemplateSerializer(serializers.ModelSerializer):
    name = InvestmentNameSerializer(many=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentName.objects.all(), source='name', write_only=True,
        allow_null=True)

    investment_class = InvestmentClassSerializer(many=False, read_only=True)
    investment_class_id = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentClass.objects.all(),
        source='investment_class',
        write_only=True,
        allow_null=True)


    class Meta:
        model = Investment
        fields = "__all__"


class AssetAllocationTemplateSerializer(serializers.ModelSerializer):
    name = AssetAllocationNameSerializer(many=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetAllocationName.objects.all(), source='name',
        write_only=True,
        allow_null=True)

    class Meta:
        model = AssetAllocation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AssetAllocationTemplateSerializer, self).__init__(*args, **kwargs)
        if "investment_id" in self.context:
            investment_id = self.context["investment_id"]
            self.fields['investment'].queryset = Investment.objects.filter(id=investment_id)
