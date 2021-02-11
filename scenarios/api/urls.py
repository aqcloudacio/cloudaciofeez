from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from scenarios.api import views

app_name = "scenarios"

router = SimpleRouter()

router.register(r"scenarios", views.ScenarioViewSet, "scenarios")

scenario_router = routers.NestedSimpleRouter(router,
                                             r'scenarios',
                                             lookup='scenario')

scenario_router.register(r'reports',
                         views.ReportViewSet,
                         'reports')

# api/scenarios/$scenarioId/aasummary/
scenario_router.register(r'aasummary',
                         views.ScenarioAASummaryViewset,
                         'aasummary')

urlpatterns = [
    path("", include(router.urls)),

    path("", include(scenario_router.urls)),

    ]
