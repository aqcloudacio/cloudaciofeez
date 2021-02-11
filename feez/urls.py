"""feez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django_registration.backends.one_step.views import RegistrationView
from users.forms import UserCreateForm
from core.views import IndexTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/register/', RegistrationView.as_view(
    #                             form_class=UserCreateForm,
    #                             success_url="/",
    #                             ), name="django_registration_register"),
    # path('accounts/', include("django_registration.backends.one_step.urls")),
    # path('accounts/', include("django.contrib.auth.urls")),
    # path('accounts/', include("allauth.urls")),

    path('api/', include("users.api.urls")),
    path('api/', include("platforms.api.urls")),
    path('api/', include("scenarios.api.urls")),
    path('api/', include("portfolios.api.urls")),
    path('api/', include("investments.api.urls")),
    path('api/', include("riskprofiles.api.urls")),
    path('api/', include("documents.api.urls")),
    path('api/', include("scrapes.api.urls")),
    path('api/', include("adverts.api.urls")),

    # path('api-auth/', include("rest_framework.urls")),
    # path('api/rest-auth/', include("rest_auth.urls")),
    # path('api/rest-auth/registration/', include("rest_auth.registration.urls")),

    # path('app/',IndexTemplateView.as_view(), name="entry-point")

    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")]

# Note - routing via /app or /profile, etc is done via vue router.
