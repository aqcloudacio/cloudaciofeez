from rest_framework import viewsets
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q

from rest_framework.permissions import IsAuthenticated

from scenarios.api.permissions import IsOwner, IsSharedPractice

from scenarios.api.serializers import ScenarioSerializer, ReportSerializer

from scenarios.models import Scenario, Report
from riskprofiles.models import RiskProfileAAName
from riskprofiles.api.serializers import RiskProfileAANameSerializer
User = get_user_model()


class ScenarioViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = ScenarioSerializer
    permission_classes = [IsOwner | IsSharedPractice, IsAuthenticated]

    def get_queryset(self):
        '''
        Returns all Scenarios that:
        1. Are owned by the current user (user=user)
        2. Have a Practice assigned that is == current user's active_practice,
           regardless of the actual owner of that Scenario (if there is one).
        3. Have been explicitly shared via the allowed_users field

        Note: If the user does not have an active_practice set, they are unable
        to see scenarios that are owned by a specific practice via
        scenario.practice
        '''
        user = self.request.user
        active_practice = self.request.user.active_practice
        practices = self.request.user.practices.all()
        if active_practice:
            return Scenario.objects.filter(Q(user=user)
                                           | Q(allowed_users__in=[user])
                                           | (Q(practice=active_practice)
                                              & Q(practice__in=practices))).distinct()
        else:
            return Scenario.objects.filter((Q(user=user)
                                            & Q(practice__isnull=True))
                                           | Q(allowed_users__in=[user]))


class ReportViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        scenario_id = self.kwargs.get("scenario_id")
        return Report.objects.filter(scenario=scenario_id).order_by("-created_at")


class ScenarioAASummaryViewset(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = RiskProfileAANameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        scenario_id = self.kwargs.get("scenario_id")
        scenario = get_object_or_404(Scenario, id=scenario_id)
        group = scenario.risk_profile.group

        return RiskProfileAAName.objects.filter(group=group).order_by("order")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["scenario_id"] = self.kwargs["scenario_id"]
        return context
