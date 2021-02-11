from django.urls import include, path
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter

from scenarios.api.urls import router

from documents.api import views

app_name = "documents"

scenario_router = routers.NestedSimpleRouter(router,
                                             r'scenarios',
                                             lookup='scenario')

scenario_router.register(r'themes',
                         views.ThemeViewSet,
                         'themes')


theme_router = routers.NestedSimpleRouter(scenario_router,
                                             r'themes',
                                             lookup='theme')

theme_router.register(r'styles',
                         views.StyleViewSet,
                         'styles')

theme_router.register(r'structures',
                         views.StructureViewSet,
                         'structures')

theme_router.register(r'content',
                         views.ContentViewSet,
                         'content')

style_router = routers.NestedSimpleRouter(theme_router,
                                          r'styles',
                                          lookup='style')

style_router.register(r'elements',
                      views.ElementViewSet,
                      'elements')

##############
# Routers for helper views
##############

#
# templaterouter = SimpleRouter()
# # /api/themelist
# # DO NOT use this view for looking up single themes
# templaterouter.register(r"themelist",
#                         views.ThemeListViewSet,
#                         "themelist")
#
# ##############
# Routers for templates
##############

templaterouter = SimpleRouter()
templaterouter.register(r"themes",
                        views.ThemeTemplateViewSet,
                        "themes")


theme_template_router = routers.NestedSimpleRouter(templaterouter,
                                                      r'themes',
                                                      lookup='theme')

theme_template_router.register(r"styles",
                                  views.StyleViewSet,
                                  "styles")

theme_template_router.register(r"content",
                                  views.ContentViewSet,
                                  "content")

theme_template_router.register(r"structures",
                                  views.StructureViewSet,
                                  "structures")


style_template_router = routers.NestedSimpleRouter(theme_template_router,
                                                   r'styles',
                                                   lookup='style')

style_template_router.register(r'elements',
                              views.ElementViewSet,
                              'elements')


urlpatterns = [
    path("",
         include(scenario_router.urls)),

    path("",
         include(theme_router.urls)),

    path("",
         include(style_router.urls)),

    path("",
         include(templaterouter.urls)),

    path("",
         include(theme_template_router.urls)),

    path("",
         include(style_template_router.urls)),
    ]
