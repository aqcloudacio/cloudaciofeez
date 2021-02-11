from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from scenarios.api.urls import router

from platforms.api import views
from investments.api.views import InvestmentAASummaryViewset


app_name = "platforms"

scenario_router = routers.NestedSimpleRouter(router,
                                             r'scenarios',
                                             lookup='scenario')

scenario_router.register(r'platforms',
                         views.PlatformViewSet,
                         'platforms')

platform_router = routers.NestedSimpleRouter(scenario_router,
                                             r'platforms',
                                             lookup='platform')

platform_router.register(r'platformfees',
                         views.PlatformFeeViewSet,
                         'platformfees')


platform_fee_router = routers.NestedSimpleRouter(platform_router,
                                                 r'platformfees',
                                                 lookup='platformfee')

platform_fee_router.register(r'tier-thresholds',
                             views.PlatformTierThresholdViewSet,
                             "tier-thresholds")

platform_fee_router.register(r'tier-percs',
                             views.PlatformTierPercViewSet,
                             "tier-percs")

rootrouter = SimpleRouter()
rootrouter.register(r"platformnames",
                    views.PlatformNameViewSet,
                    "platformnames")

# rootrouter.register(r"platforms",
#                     views.PlatformViewSet,
#                     "platforms")

rootrouter.register(r"platformfamilygroups",
                    views.PlatformFamilyGroupsViewSet,
                    "platformfamilygroups")

#############
# Helper/shortcut routers
#############

platform_name_router = routers.NestedSimpleRouter(rootrouter,
                                                    r'platformnames',
                                                    lookup='platformname')
# api/platformnames/$platformnameid/investmentnames/
platform_name_router.register(r'investmentnames',
                         views.PlatformNameInvestmentNameViewSet,
                         'investmentnames')

# api/platforms/$platformid/aa/
platform_router.register(r'aa',
                         views.PlatformAAViewSet,
                         'aa')

# api/platforms/$platformid/aasummary/
platform_router.register(r'aasummary',
                         views.PlatformAASummaryViewset,
                         'aasummary')

# api/platforms/$platformid/investments/
platform_router.register(r'investments',
                         views.PlatformInvestmentViewSet,
                         'investments')

# api/platforms/$platformid/portfolios/
platform_router.register(r'portfolios',
                         views.PlatformPortfolioViewSet,
                         'portfolios')

platform_investment_router = routers.NestedSimpleRouter(platform_router,
                                                        r'investments',
                                                        lookup='investment')
# api/platforms/$platformid/investments/$investmentid/aa
platform_investment_router.register(r'aa',
                                    views.PlatformInvestmentAAViewSet,
                                    'aa')

# api/platforms/$platformid/investments/$investmentid/aasummary
platform_investment_router.register(r'aasummary',
                                    InvestmentAASummaryViewset,
                                    'aasummary')


##############
# Routers for templates
##############

templaterouter = SimpleRouter()
templaterouter.register(r"platformtemplates",
                        views.PlatformTemplateViewSet,
                        "platformtemplates")

platform_template_router = routers.NestedSimpleRouter(templaterouter,
                                                      r'platformtemplates',
                                                      lookup='platformtemplate')

platform_template_router.register(r'fees',
                                  views.PlatformFeeTemplateViewSet,
                                  "platform-thresholds")

platform_fee_template_router = routers.NestedSimpleRouter(platform_template_router,
                                                          r'fees',
                                                          lookup='platformfeetemplate')

platform_fee_template_router.register(r'tier-thresholds',
                                      views.PlatformTierThresholdTemplateViewSet,
                                      "tier-thresholds")

platform_fee_template_router.register(r'tier-percs',
                                      views.PlatformTierPercTemplateViewSet,
                                      "tier-percs")


urlpatterns = [
    path("",
         include(scenario_router.urls)),

    path("",
         include(platform_router.urls)),

    path("",
         include(platform_fee_router.urls)),

    path("",
         include(platform_investment_router.urls)),

    path("",
         include(rootrouter.urls)),

    path("",
         include(platform_name_router.urls)),

    path("",
         include(templaterouter.urls)),

    path("",
         include(platform_template_router.urls)),

    path("",
         include(platform_fee_template_router.urls)),
    ]
