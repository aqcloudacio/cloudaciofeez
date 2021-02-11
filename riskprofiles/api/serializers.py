from rest_framework import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Sum

from riskprofiles.models import (RiskProfile, RiskProfileAAName, RiskProfileAA,
                                 RiskProfileGroup, RiskProfileAAName)
from scenarios.models import Scenario
from investments.models import AssetAllocation
from users.models import Practice, AFSL
from investments.models import Investment
from platforms.models import Platform



class RiskProfileGroupSerializer(serializers.ModelSerializer):

    active_practices = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(),
                                                          many=True, allow_null=True)
    afsls = serializers.PrimaryKeyRelatedField(queryset=AFSL.objects.all(),
                                                many=True, allow_null=True,
                                                required=False)

    class Meta:
        model = RiskProfileGroup
        fields = "__all__"


class RiskProfileAANameSerializer(serializers.ModelSerializer):

    aa_total_perc = serializers.SerializerMethodField()
    aa_total_perc_platform = serializers.SerializerMethodField()
    aa_total = serializers.SerializerMethodField()

    cur_total_perc = serializers.SerializerMethodField()
    rec_total_perc = serializers.SerializerMethodField()
    alt_total_perc = serializers.SerializerMethodField()

    cur_total = serializers.SerializerMethodField()
    rec_total = serializers.SerializerMethodField()
    alt_total = serializers.SerializerMethodField()



    class Meta:
        model = RiskProfileAAName
        fields = "__all__"

    def get_aa_total_perc(self, obj):
        if "investment_id" in self.context:
            id = self.context["investment_id"]
            investment = get_object_or_404(Investment, id=id)
            if investment.amount:
                return self.get_aa_total(obj) / investment.amount
            else:
                return None

    def get_aa_total_perc_platform(self, obj):
        if "platform_id" in self.context:
            id = self.context["platform_id"]
            platform = get_object_or_404(Platform, id=id)
            if platform.platform_total:
                return self.get_aa_total(obj) / platform.platform_total
            else:
                return None


    def get_aa_total(self, obj):
        if "investment_id" in self.context or "platform_id" in self.context:
            # Gets the template RP AA Name (all investments are linked to a
            # default templated RP AA name)
            rp_aaname_template = get_object_or_404(RiskProfileAAName,
                                                    template=True,
                                                    name=obj.name)

            if "investment_id" in self.context:
                id = self.context["investment_id"]
                try:
                    # Gets the assetallocation objects that are linked to this
                    # investment and that match the templated rp_aa_name that is linked to this user's set of
                    # rp_aa_names
                    aa_list = AssetAllocation.objects.filter(investment=id,
                                                             name__rp_aaname_link=rp_aaname_template)
                except Exception as e:
                    print(e)


            elif "platform_id" in self.context:
                id = self.context["platform_id"]
                try:
                    # Gets the assetallocation objects that are linked to this
                    # platform (via their investments) and that match the
                    # templated rp_aa_name that is linked to this user's set of
                    # rp_aa_names
                    aa_list = AssetAllocation.objects.filter(investment__platform=id,
                                                             name__rp_aaname_link=rp_aaname_template)
                except Exception as e:
                    print(e)

            if id:
                total = 0
                for aa in aa_list:
                    total += aa.aa_dollar
                return total

    def get_cur_total_perc(self,obj):
        if "scenario_id" in self.context:
            id = self.context["scenario_id"]
            scenario = get_object_or_404(Scenario, id=id)
            if scenario.scenario_total_cur:
                return self.get_cur_total(obj) / scenario.scenario_total_cur
            else:
                return None

    def get_rec_total_perc(self,obj):
        if "scenario_id" in self.context:
            id = self.context["scenario_id"]
            scenario = get_object_or_404(Scenario, id=id)
            if scenario.scenario_total_rec:
                return self.get_rec_total(obj) / scenario.scenario_total_rec
            else:
                return None

    def get_alt_total_perc(self,obj):
        if "scenario_id" in self.context:
            id = self.context["scenario_id"]
            scenario = get_object_or_404(Scenario, id=id)
            if scenario.scenario_total_alt:
                return self.get_alt_total(obj) / scenario.scenario_total_alt
            else:
                return None

    def get_cur_total(self, obj):
        return self.total_getter(obj, "Current")

    def get_rec_total(self, obj):
        return self.total_getter(obj, "Recommended")

    def get_alt_total(self, obj):
        return self.total_getter(obj, "Alternative")

    def total_getter(self, obj, status):
        if "scenario_id" in self.context:
            scenario_id = self.context["scenario_id"]
            # Gets the template RP AA Name (all investments are linked to a
            # default templated RP AA name)
            rp_aaname_template = get_object_or_404(RiskProfileAAName,
                                                    template=True,
                                                    name=obj.name)
            try:
                # Gets the assetallocation objects that are linked to this
                # scenario (via their investments) and that match the
                # templated rp_aa_name that is linked to this user's set of
                # rp_aa_names
                aa_list = AssetAllocation.objects.filter(investment__platform__scenario=scenario_id,
                                                         investment__platform__status=status,
                                                         name__rp_aaname_link=rp_aaname_template)
                total = 0
                for aa in aa_list:
                    total += aa.aa_dollar
                return total
            except Exception as e:
                print(e)


class RiskProfileAASerializer(serializers.ModelSerializer):

    name = RiskProfileAANameSerializer(many=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(
        queryset=RiskProfileAAName.objects.all(), source='name', write_only=True)
    name_order = serializers.ReadOnlyField()


    class Meta:
        model = RiskProfileAA
        fields = "__all__"


class RiskProfileSerializer(serializers.ModelSerializer):

    allocations = serializers.SerializerMethodField()


    class Meta:
        model = RiskProfile
        fields = "__all__"

    def get_allocations(self,obj):
        queryset = obj.allocations.all().order_by('name__order')
        return RiskProfileAASerializer(queryset, many=True, read_only=True).data
