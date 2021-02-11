from django.conf import settings

from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import AFSL, Practice, Notification
from django.shortcuts import get_object_or_404
from documents.models import Theme
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.password_validation import (validate_password,
                                                     get_password_validators)
from django.core.exceptions import ValidationError

from riskprofiles.api.serializers import RiskProfileGroupSerializer

User = get_user_model()

# Shared Functions across a couple of serializers
def send_verification_email(instance, AFSL_data):
    '''
    Sends verification email to ProductRex support.
    Currently uses Google SMTP via setttings. May need changing to SendGrid
    or similar in the future.
    '''
    send_mail(
        'AFSL verification',
        f'The user {instance.email} has added an AFSL ({AFSL_data["AFSL_number"]}) to their account.\
        Log in and verify the account.',
        settings.EMAIL_HOST_USER,
        ['nftopham@gmail.com'],
        fail_silently=False,
    )

def create_or_link_AFSL(AFSL_data, validated_data):
    validated_data['AFSL_approved'] = False

    try:
        existing_AFSL = get_object_or_404(AFSL, AFSL_number=AFSL_data['AFSL_number'])
        validated_data['AFSL'] = existing_AFSL

    except Exception:
        new_AFSL = AFSL.objects.create(AFSL_number=AFSL_data['AFSL_number'])
        new_AFSL.save()
        validated_data['AFSL'] = new_AFSL

    return validated_data



class EmailAndNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "name", "id")
        # WARNING. The email validators have been disabled so that this
        # serializer can be used as a nested serializer.
        # It should NOT be used to create or update user instances.
        extra_kwargs = {
            'email': {'validators': []},
        }

class AFSLSerializer(serializers.ModelSerializer):

    class Meta:
        model = AFSL
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"


class PracticeSerializer(serializers.ModelSerializer):

    staff = EmailAndNameSerializer(read_only=True, many=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='staff', many=True,
        write_only=True, allow_null=True)

    admins = EmailAndNameSerializer(read_only=True, many=True)
    admins_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='admins', many=True,
        write_only=True, allow_null=True)

    pending_staff = EmailAndNameSerializer(read_only=True, many=True)
    pending_staff_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='pending_staff', many=True,
        write_only=True, allow_null=True)

    AFSL_full = AFSLSerializer(many=False, required=False, allow_null=True,
                                read_only=True, source='AFSL')
    RPG_full = RiskProfileGroupSerializer(many=False, required=False, allow_null=True,
                                read_only=True, source='risk_profile_group')
    class Meta:
        model = Practice
        fields = "__all__"

    def update(self, instance, validated_data):
        '''
        Modified to allow adding of users to a practice/sending emails and
        and notifications
        '''
        if 'add_staff' in validated_data:
            inviter = self.context['request'].user
            add_staff = validated_data.pop('add_staff')
            practice = super().update(instance, validated_data)

            if add_staff:
                try:
                    found = get_object_or_404(User, email=add_staff)
                    found.pending_practices.add(instance)
                    found.save()
                    self.add_staff_notification(inviter, found, instance)

                except Exception:
                    # If they don't exist, send an email invite to them to ProductRex
                    self.send_invite_email(inviter, add_staff, instance)
                    self.add_staff_notification(inviter, add_staff, instance)

                    error = {'message': "This email does not have a ProductRex account. An invitation has been sent."}
                    raise serializers.ValidationError(error)

        else:
            practice = super().update(instance, validated_data)

        return practice

    def get_inviter(self,inviter):
        '''
        If the inviter has no name, insert their email in the email/notification.
        '''
        if inviter.name:
            return inviter.name
        else:
            return inviter.email

    def add_staff_notification(self, inviter, user, practice):
        '''
        Creates a new notification when a user is added to a practice. Allows the
        added user to accept the invitation.
        '''
        if isinstance(user, str):
            #If no account exists
            try:
                notification = Notification(title="Practice Invitation",
                                            content=f"{self.get_inviter(inviter)} has invited you to join {practice.name}",
                                            type="practice_invite",
                                            read=False,
                                            to=user,
                                            practice=practice)
                notification.save()

            except Exception as e:
                print(e)
        else:
            #If account exists.
            try:
                notification = Notification(title="Practice Invitation",
                                            content=f"{self.get_inviter(inviter)} has invited you to join {practice.name}",
                                            type="practice_invite",
                                            read=False,
                                            target=user,
                                            practice=practice)
                notification.save()

            except Exception as e:
                print(e)

    def send_invite_email(self, inviter, user, practice):
        send_mail(
            f'{self.get_inviter(inviter)} wants you to join {practice.name} on ProductRex.',
            f'{self.get_inviter(inviter)} wants to invite you to join {practice.name} on ProductRex. \
            As you do not yet have a ProductRex account, you must create \
            one to join this practice.',
            settings.EMAIL_HOST_USER,
            [user],
            fail_silently=False,
        )


class UserSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField()
    practice_names = serializers.SerializerMethodField()
    active_practice_name = serializers.SerializerMethodField()
    active_theme_name = serializers.SerializerMethodField()
    active_rp_name = serializers.ReadOnlyField()
    AFSL = AFSLSerializer(many=False, required=False, allow_null=True)
    # multiple_rpgs = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ["password", "date_joined", "last_login"]


    def update(self, instance, validated_data):
        '''
        Modified to allow updating of AFSL number via the user serializer.
        '''
        AFSL_data = validated_data.pop('AFSL')

        if AFSL_data:
            if instance.AFSL:
                if getattr(instance.AFSL,"AFSL_number","") != AFSL_data["AFSL_number"]:
                    # AFSL number has  changed
                    validated_data = create_or_link_AFSL(AFSL_data, validated_data)
                    send_verification_email(instance, AFSL_data)
                else:
                    # AFSL number has not changed, no action required.
                    pass

            else:
                # No AFSL currently linked, set up a new link and send email
                validated_data = create_or_link_AFSL(AFSL_data, validated_data)
                send_verification_email(instance, AFSL_data)

        user = super().update(instance, validated_data)

        return user




    def get_practice_names(self, obj):
        result = []
        if obj.practices.all():
            for practice in obj.practices.all():
                print(practice)
                result.append(practice.name);
                return result
        else:
            return None

    def get_active_practice_name(self,obj):

        if obj.active_practice:
            try:
                practice = get_object_or_404(Practice, id=obj.active_practice.id)
                return practice.name

            except Exception as e:
                print(e)

    def get_active_theme_name(self,obj):

        if obj.active_theme:
            try:
                theme = get_object_or_404(Theme, id=obj.active_theme.id)
                return theme.name

            except Exception as e:
                print(e)


class RegoDetailsSerializer(serializers.ModelSerializer):

    AFSL = AFSLSerializer(many=False, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "role", "linked_ARN", "AFSL"]
        extra_kwargs = {'first_name': {'write_only': True},
                        'last_name': {'write_only': True},
                        'phone': {'write_only': True},
                        'role': {'write_only': True},
                        'linked_ARN': {'write_only': True},
                        'AFSL': {'write_only': True},
                        'id': {'read_only': False}}

    def update(self, instance, validated_data):
        '''
        Modified to allow updating of AFSL number via the user serializer.
        '''
        AFSL_data = validated_data.pop('AFSL')

        if AFSL_data:
            # No AFSL currently linked, set up a new link and send email
            validated_data = create_or_link_AFSL(AFSL_data, validated_data)
            send_verification_email(instance, AFSL_data)

        user = super().update(instance, validated_data)

        return user


class RegoSerializer(serializers.ModelSerializer):

    user_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["email", "password", "user_id"]
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': False}}

    def create(self, validated_data):
        '''
        Registers a new user and sends them an email with a verification token.
        '''
        email = validated_data['email']

        user = User.objects.create(email=email,
                                   is_active=False)
        user.set_password(validated_data['password'])
        user.save()

        token = default_token_generator.make_token(user)
        self.send_confirmation_email(user, token)
        return user

    def update(self, instance, validated_data):
        '''
        Used to re-send verification tokens if the user requets a new one (for
        example, if it has expired.)
        '''

        token = default_token_generator.make_token(instance)
        self.send_confirmation_email(instance, token)

        return super().update(instance, validated_data)

    def send_confirmation_email(self, user, token):
        '''
        Sends confirmation email to user.
        Currently uses Google SMTP via setttings. May need changing to SendGrid
        or similar in the future.
        '''
        uid = urlsafe_base64_encode(force_bytes(user.id))

        send_mail(
            'Verify your ProductRex account',
            f'Thank you for creating a ProductRex account. To confirm and \
            activate your account, please click the link below: \
            \
            http://127.0.0.1:8000/verify/{user.id}/{token}/\
            \
            Your verification code: {token}\
            \
            Please note that this code is only valid for 3 days.\
            \
            Thanks\
            ProductRex Support',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

    def get_user_id(self, instance):
        if instance.id:
            return instance.id

class ResetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email"]


    def update(self, instance, validated_data):
        '''
        Searches for a given email and sends token in email if it exists.
        NOTE: Does NOT create a user
        '''

        email = validated_data['email']

        try:
            user = get_object_or_404(User, email=email)
            print("user found")
            token = default_token_generator.make_token(user)
            self.send_reset_email(user, token, 'success')

        except Exception as e:
            print("user not found")
            self.send_reset_email(email, token, 'failure')

        return super().update(instance, validated_data)


    def send_reset_email(self, user, token, status):
        '''
        Sends email reset email to user.
        Currently uses Google SMTP via setttings. May need changing to SendGrid
        or similar in the future.
        '''
        uid = urlsafe_base64_encode(force_bytes(user.id))

        if status == 'success':
            content =  f'You have requested a password reset on your ProductRex \
                        account. To reset your password, please click the link below and follow the instructions on the page. \
                        \
                        http://127.0.0.1:8000/verifyreset/{user.id}/{token}/\
                        \
                        Your verification code: {token}\
                        \
                        Please note that this code is only valid for 3 days.\
                        \
                        Thanks\
                        ProductRex Support'
        else:
            content =   f'You (or someone else) entered this email address when \
                        trying to to change the password of a ProductRex account.\
                        \
                        However, this email is not on our database of registered users,\
                        so the password reset has failed.\
                        \
                        If you are a ProductRex user, please attempt a password reset using the same email address you gave when opening your account.\
                        \
                        If you are not a ProductRex user, please ignore this email.\
                        \
                        For more information about ProductRex, visit www.productrex.com.au\
                        \
                        Thanks\
                        ProductRex Support'

        send_mail(
            'Reset your ProductRex password',
            content,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "password"]
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': False}}

    def update(self, instance, validated_data):
        '''
        Searches for a given email and sends token in email if it exists.
        NOTE: Does NOT create a user
        '''
        user_id = validated_data["id"]
        password = validated_data.pop("password")


        if password:
            try:
                user = User.objects.get(id=user_id)
            except Exception:
                raise serializers.ValidationError(detail="User not found")

            try:
                validated_password = validate_password(password, user)

            except ValidationError as e:
                print(e)
                raise serializers.ValidationError(detail=e)

            user.set_password(password)
            user.save()
            return super().update(user, validated_data)

        else:
            raise serializers.ValidationError(detail="Invalid password")




class VerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "verify_token"]
        extra_kwargs = {'verify_token': {'write_only': True},
                        'id': {'read_only': False}}

    def update(self, instance, validated_data):
        '''
        Validates the given token against the given user.
        '''
        token = validated_data.pop('verify_token')

        if token:
            user_id = validated_data["id"]
            user = User.objects.get(id=user_id)
            if default_token_generator.check_token(user, token):
                if not user.is_active:
                    user.is_active = True
                    user.save()

                return super().update(user, validated_data)

            else:
                raise serializers.ValidationError(detail="Verification code is invalid")
        else:
            raise serializers.ValidationError(detail="Token not provided")
