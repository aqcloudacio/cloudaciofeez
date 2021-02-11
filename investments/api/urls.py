from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from investments.api.views import (InvestmentViewSet, InvestmentClassViewSet,
                                   AssetAllocationViewSet,
                                   AssetAllocationNameViewSet,
                                   InvestmentNameViewSet,
                                   NABInvestmentViewSet,
                                   InvestmentTemplateViewSet,
                                   AssetAllocationTemplateViewSet,
                                   UnlinkedAssetAllocationNameViewSet,
                                   UnlinkedInvestmentNameViewSet,
                                   InvestmentAASummaryViewset)

from portfolios.api.urls import platform_router

app_name = "investments"

#########
# Full length routes
#########

portfolio_router = routers.NestedSimpleRouter(platform_router,
                                              r'portfolios',
                                              lookup='portfolio')
portfolio_router.register(r'investments',
                          InvestmentViewSet,
                          'investments')

investments_router = routers.NestedSimpleRouter(portfolio_router,
                                                r'investments',
                                                lookup='investment')
investments_router.register(r'aa',
                            AssetAllocationViewSet,
                            'aa')

#########
# Template routes
#########
templaterouter = SimpleRouter()
templaterouter.register(r"investmenttemplate", InvestmentTemplateViewSet)

investment_template_router = routers.NestedSimpleRouter(templaterouter,
                                                        r'investmenttemplate',
                                                        lookup='investmenttemplate')
investment_template_router.register(r'aa',
                                    AssetAllocationTemplateViewSet,
                                    'aa')
#########
# Basename routes
#########
rootrouter = SimpleRouter()
rootrouter.register(r"investmentclass", InvestmentClassViewSet)
rootrouter.register(r"aaname", AssetAllocationNameViewSet)
rootrouter.register(r"unlinkedaaname", UnlinkedAssetAllocationNameViewSet)
# All investment names
rootrouter.register(r"investmentname", InvestmentNameViewSet)
# Only investment names that are not linked to a platform (non-specific invs)
rootrouter.register(r"unlinkedinvestmentname", UnlinkedInvestmentNameViewSet)
rootrouter.register(r"NABinvestment", NABInvestmentViewSet)


urlpatterns = [
    path("", include(portfolio_router.urls)),

    path("", include(investments_router.urls)),

    path("", include(templaterouter.urls)),

    path("", include(investment_template_router.urls)),

    path("", include(rootrouter.urls))
]
