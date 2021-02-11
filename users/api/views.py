from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


from users.api.serializers import (UserSerializer, AFSLSerializer,
                                   PracticeSerializer, NotificationSerializer,
                                   RegoSerializer, VerifySerializer,
                                   ResetPasswordSerializer,
                                   ChangePasswordSerializer,
                                   RegoDetailsSerializer)
from users.models import AFSL, Practice, Notification

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        return User.objects.filter(email=self.request.user).order_by("id")


class AFSLViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = AFSLSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return AFSL.objects.all().order_by("name")


class NotificationViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # return Notification.objects.all().order_by("-date_sent")
        return Notification.objects.filter(target=user).order_by("-date_sent")


class PracticeViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = PracticeSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        '''
        Sets the creator of the practice as both staff and admin.
        '''
        user = self.request.user
        serializer.save(staff=[user], admins=[user])
        perform_create = super().perform_create(serializer)
        return perform_create

    def get_queryset(self):
        user = self.request.user
        return Practice.objects.filter(staff__in=[user]).order_by("name")

class RegoDetailsViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = RegoDetailsSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        id = self.kwargs.get("id")
        return User.objects.filter(id=id).order_by("id")

class RegoViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = RegoSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        id = self.kwargs.get("id")
        return User.objects.filter(id=id).order_by("id")

class ResetPasswordViewSet(viewsets.ModelViewSet):

    lookup_field = 'email'
    lookup_value_regex = '[\w.@]+'
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        email = self.kwargs.get("email")
        return User.objects.filter(email=email).order_by("email")


class VerifyViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = VerifySerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        id = self.kwargs.get("id")
        return User.objects.filter(id=id).order_by("id")

class ChangePasswordViewSet(viewsets.ModelViewSet):

    lookup_field = "id"
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        id = self.kwargs.get("id")
        return User.objects.filter(id=id).order_by("id")
