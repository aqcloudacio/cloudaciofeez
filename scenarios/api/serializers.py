from rest_framework import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from scenarios.models import Scenario, Report
from platforms.models import Platform
from riskprofiles.models import RiskProfile
from riskprofiles.api.serializers import RiskProfileSerializer
from users.api.serializers import EmailAndNameSerializer
from users.models import Notification


User = get_user_model()

class ScenarioSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField()
    scenario_total = serializers.ReadOnlyField()
    risk_profile_group_name = serializers.ReadOnlyField()

    risk_profile_name = serializers.SerializerMethodField()
    platforms = serializers.SerializerMethodField()

    risk_profile = RiskProfileSerializer(many=False, read_only=True)
    risk_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=RiskProfile.objects.all(), source='risk_profile', write_only=True,
        allow_null=True)

    allowed_users = EmailAndNameSerializer(many=True, required=False)


    class Meta:
        model = Scenario
        fields = "__all__"
        extra_fields = ['platforms']

    def update(self, instance, validated_data):
        '''
        Modified to filter sharing of scenarios by email address for new and
        existing users

        '''
        if 'allowed_users' in validated_data:
            inviter = self.context['request'].user
            allowed_users_data = validated_data.pop('allowed_users')
            scenario = super().update(instance, validated_data)

            if instance.allowed_users.count() < len(allowed_users_data):
                # allowed_users has increased
                for allowed_user in [x for x in allowed_users_data if not x.get('id',False)]:
                    # filter allowed_users to only show newly shared users.
                    # If a user has been removed, this loop will be skipped
                    # as all allowed_users will have ids
                    try:
                        # search for the user by email
                        existing_allowed_user = get_object_or_404(User, email=allowed_user['email'].casefold())
                        # send a notification to the existing user
                        if instance not in existing_allowed_user.shared_scenarios.all():
                            # Prevents user receiving notifications for scenarios
                            # they have already been shared.
                            self.send_sharing_notification(inviter, existing_allowed_user, instance)
                            # adds the user to the allowed_users m2m
                            scenario.allowed_users.add(existing_allowed_user)

                    except Exception:
                        # If they don't exist, send an email invite to them to ProductRex
                        self.send_invite_email(inviter, allowed_user, instance)
                        self.send_sharing_notification(inviter, allowed_user, instance)

                        error = {'message': "This email does not have a ProductRex account. An invitation has been sent."}
                        raise serializers.ValidationError(error)

            else:
                #allowed users has decreased - reset the allowed_users
                allowed_users_list = []
                for allowed_user in allowed_users_data:
                    #Build a list of user instances
                    user = get_object_or_404(User, email=allowed_user['email'].casefold())
                    allowed_users_list.append(user)

                scenario.allowed_users.clear()
                try:
                    scenario.allowed_users.add(*allowed_users_list)
                except Exception as e:
                    print(e)
        else:
            scenario = super().update(instance, validated_data)

        return scenario


    def send_sharing_notification(self, inviter, allowed_user, instance):
        if getattr(allowed_user,'id',False):
            try:
                notification = Notification(title=f"You now have access to {instance.client}",
                                            content=f"{inviter.name} has shared the scenario for {instance.client} with you.",
                                            type="scenario_share",
                                            read=False,
                                            target=allowed_user)
                notification.save()
            except Exception as e:
                print(e)
        else:
            # The user does not have an account, create a notification but use
            # the "to" field instead of target. Will be assigned on acc creation.

            # Assignment of notification on account creation must also add them
            # as an allowed_user using the newly created user instance.
            try:

                notification = Notification(title=f"You now have access to {instance.client}",
                                            content=f"{inviter.name} has shared the scenario for {instance.client} with you.",
                                            type="scenario_share",
                                            read=False,
                                            to=allowed_user['email'])
                notification.save()
            except Exception as e:
                print(e)



    def send_invite_email(self, inviter, allowed_user, instance):
        send_mail(
            f'{inviter.name} wants to share ProductRex for {instance.client}',
            f'The user {inviter.name} wants to share {instance.client}\
            with you. As you do not have a ProductRex account, you must create \
            one to view this client',
            settings.EMAIL_HOST_USER,
            [allowed_user['email']],
            fail_silently=False,
        )

    def get_platforms(self, obj):
        if obj.platforms.exists():
            platforms = obj.platforms.all()
            platform_names = []
            for platform in platforms:
                if platform.custom_name:
                    link = (platform.id, platform.custom_name, platform.status)
                else:
                    if platform.name:
                        link = (platform.id, platform.name.name, platform.status)
                platform_names.append(link)

            try:
                platform_names = sorted(platform_names, key=lambda x: x[1])
                return platform_names
            except Exception as e:
                print(e)
        else:
            return None

    def get_risk_profile_name(self,obj):
        if obj.risk_profile:
            rp = get_object_or_404(RiskProfile,
                                   id=obj.risk_profile.id)
            return rp.name



class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = "__all__"
