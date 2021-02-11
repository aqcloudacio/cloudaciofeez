from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models.query_utils import Q


from documents.api.serializers import (ThemeSerializer, StyleSerializer,
                                       StructureSerializer, ElementSerializer,
                                       ContentSerializer)
from documents.models import Theme, Style, Structure, Element, Content

###############
# Non-template viewsets
###############

def get_user_AFSL(user):
    if user.AFSL_approved:
        return user.AFSL
    else:
        return None

class ThemeViewSet(viewsets.ModelViewSet):
    '''
    User accesses a specific scenario theme. They get access if they have
    accesss to the scenario (permissions/filtering in Scenario view)
    '''
    lookup_field = "id"
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        scenario_id = self.kwargs.get("scenario_id")
        return Theme.objects.filter(scenarios__in=[scenario_id],
                                    user=user).order_by("id")

class StyleViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = StyleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        theme_id = self.kwargs.get("theme_id")
        return Style.objects.filter(theme=theme_id).order_by("id")


class StructureViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = StructureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        theme_id = self.kwargs.get("theme_id")
        return Structure.objects.filter(theme=theme_id).order_by("id")


class ContentViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        theme_id = self.kwargs.get("theme_id")
        return Content.objects.filter(theme=theme_id).order_by("table_type", "order")


class ElementViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = ElementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        style_id = self.kwargs.get("style_id")
        return Element.objects.filter(style=style_id).order_by("type")


# ###############
# # Helper viewsets
# ###############
#
# class ThemeListViewSet(viewsets.ModelViewSet):
#
#     lookup_field = "id"
#     serializer_class = ThemeSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         AFSL = get_user_AFSL(user)
#         practices = user.practices.all()
#
#         return Theme.objects.filter(Q(user=user)
#                                     | Q(afsls__in=[AFSL])
#                                     | Q(active_practices__in=practices)
#                                     | Q(default=True),
#                                     template=True).order_by("id")
#
# ###############
# Template viewsets
###############

class ThemeTemplateViewSet(viewsets.ModelViewSet):
    '''
    For accessing all allowed templates (for example, from the Profile
    view). They are allowed access if:
       - They are specifically assigned to the theme (they created it)
       - The Theme is assigned to any of their practices
       - The Theme is assigned to their AFSL
       - The Theme is assigned to the AFSL that is linked to their active_prac
       - It is a default Theme (created by ProductRex)

    Note: users can not edit the default template. Limited on frontend
    '''
    lookup_field = "id"
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        AFSL = get_user_AFSL(user)
        practices = user.practices.all()
        active_practice = user.active_practice

        # Show all themes to the superuser, limit for regular users
        if user.is_superuser:
            return Theme.objects.filter(template=True).order_by("id")
        else:
            return Theme.objects.filter(Q(user=user)
                                    | Q(afsls__in=[AFSL])
                                    | Q(active_practices__in=practices)
                                    | Q(default=True)
                                    | Q(afsls__active_practices__in=[active_practice]),
                                    template=True).order_by("id")
