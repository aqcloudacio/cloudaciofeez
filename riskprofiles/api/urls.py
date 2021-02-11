from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from riskprofiles.api import views

app_name = "riskprofiles"

rpgrouprouter = SimpleRouter()

rpgrouprouter.register(r'riskprofilegroups',
                       views.RiskProfileGroupViewSet,
                       'riskprofilegroups')

rprouter = routers.NestedSimpleRouter(rpgrouprouter,
                                      r'riskprofilegroups',
                                      lookup='riskprofilegroup')

rprouter.register(r'riskprofiles',
                  views.RiskProfileViewSet,
                  'riskprofiles')

rprouter.register(r"riskprofilenames",
                  views.RiskProfileAANameViewSet,
                  'riskprofilenames')

rp_aa_router = routers.NestedSimpleRouter(rprouter,
                                          r'riskprofiles',
                                          lookup='riskprofile')
rp_aa_router.register(r'aa',
                      views.RiskProfileAAViewSet,
                      'aa')

#########
# Helper routes
#########
activeaanamerouter = SimpleRouter()

activeaanamerouter.register(r"activeriskprofilenames",
                              views.ActiveAANameViewSet,
                              'activeriskprofilenames')

#########
# Template routes
#########
rptemplaterouter = SimpleRouter()

rptemplaterouter.register(r"riskprofilenametemplates",
                              views.RiskProfileAANameTemplateViewSet,
                              'riskprofilenametemplates')

rptemplaterouter.register(r"riskprofiledefaultnametemplates",
                              views.RiskProfileDefaultAANameTemplateViewSet,
                              "riskprofiledefaultnametemplates")

rptemplaterouter.register(r"riskprofilegrouptemplates",
                          views.RiskProfileGroupTemplateViewSet,
                          "riskprofilegrouptemplates")


urlpatterns = [
    path("", include(rpgrouprouter.urls)),

    path("", include(rprouter.urls)),

    path("", include(rp_aa_router.urls)),

    path("", include(activeaanamerouter.urls)),

    path("", include(rptemplaterouter.urls))
    ]
