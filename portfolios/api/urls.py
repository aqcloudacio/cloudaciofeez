from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from portfolios.api import views

from platforms.api.urls import platform_router

app_name = "portfolios"

platform_router.register(r'portfolios',
                         views.PortfolioViewSet,
                         'portfolios')

#########
# Template routes
#########
templaterouter = SimpleRouter()
templaterouter.register(r"portfoliotemplates", views.PortfolioTemplateViewSet,
                        basename="portfoliotemplates")

model_investment_router = routers.NestedSimpleRouter(templaterouter,
                                                     r'portfoliotemplates',
                                                     lookup='portfoliotemplate')
model_investment_router.register(r'investments',
                                 views.ModelInvestmentViewSet,
                                 'investments')

urlpatterns = [
    path("", include(platform_router.urls)),

    path("", include(templaterouter.urls)),

    path("", include(model_investment_router.urls))
    ]
