from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from portfolios.api.serializers import (PortfolioSerializer,
                                        ModelInvestmentSerializer,
                                        PortfolioTemplateSerializer)

from portfolios.models import Portfolio, ModelInvestment


def get_user_AFSL(user):
    if user.AFSL_approved:
        return user.AFSL
    else:
        return None


class PortfolioViewSet(viewsets.ModelViewSet):
    '''
    Returns portfolios that are in use under the given platform.
    '''
    lookup_field = "id"
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        platform_id = self.kwargs.get("platform_id")
        return Portfolio.objects.filter(platform=platform_id).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["platform_id"] = self.kwargs["platform_id"]
        return context


###########
# Template viewsets
###########

class PortfolioTemplateViewSet(viewsets.ModelViewSet):
    '''
    Shows portfolio templates where:
       - They are specifically assigned to the model portfolio (they created it)
       - The portfolio is assigned to any of their practices
       - The portfolio is assigned to their AFSL
       - The portfolio is assigned to the AFSL that is linked to their active_prac
       - It is a "master template" portfolio (created by ProductRex)
    '''

    lookup_field = "id"
    serializer_class = PortfolioTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        AFSL = get_user_AFSL(user)
        practices = user.practices.all()
        active_practice = user.active_practice

        if user.is_superuser:
            return Portfolio.objects.filter(template=True).order_by("id")
        else:
            return Portfolio.objects.filter(Q(allowed_users__in=[user])
                                        | Q(afsls__in=[AFSL])
                                        | Q(active_practices__in=practices)
                                        | Q(master_template=True)
                                        | Q(afsls__active_practices__in=[active_practice]),
                                        template=True).order_by("name")


class ModelInvestmentViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = ModelInvestmentSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        portfolio_id = self.kwargs.get("portfoliotemplate_id")
        return ModelInvestment.objects.filter(portfolio=portfolio_id).order_by("investment_name")
