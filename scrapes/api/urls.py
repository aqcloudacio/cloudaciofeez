from django.urls import include, path
from rest_framework.routers import SimpleRouter

from scrapes.api import views

app_name = "scrapes"

router = SimpleRouter()

router.register(r"investmentscrapes", views.InvestmentScrapeViewSet, "investmentscrapes")
router.register(r"investmentscrapesettings", views.InvestmentScrapeSettingsViewSet, "investmentscrapesettings")
router.register(r"camelotsettings", views.CamelotSettingsViewSet, "camelotsettings")
router.register(r"platformscrapesettings", views.PlatformScrapeSettingsViewSet, "platformscrapesettings")
router.register(r"aplscrapesettings", views.AplScrapeSettingsViewSet, "aplscrapesettings")

urlpatterns = [
    path("", include(router.urls)),

    ]
