from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from riskprofiles.models import RiskProfile,RiskProfileGroup
from portfolios.models import Portfolio
from documents.models import Theme


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AFSL(models.Model):

    name = models.CharField(max_length=200, blank=True, null=True)
    AFSL_number = models.IntegerField(blank=True, null=True)
    theme = models.ForeignKey(Theme,
                              on_delete=models.SET_NULL,
                              related_name="afsls",
                              blank=True, null=True)
    risk_profile_group = models.ForeignKey(RiskProfileGroup,
                                           on_delete=models.SET_NULL,
                                           related_name="afsls",
                                           blank=True, null=True)
    model_portfolios = models.ManyToManyField(Portfolio,
                                              related_name="afsls",
                                              blank=True)
    # Platform fee discounts/links are a FK from the platform fee model.


class Practice(models.Model):

    name = models.CharField(max_length=200)

    risk_profile_group = models.ForeignKey(RiskProfileGroup,
                                           on_delete=models.SET_NULL,
                                           related_name="active_practices",
                                           blank=True, null=True)
    theme = models.ForeignKey(Theme,
                              on_delete=models.SET_NULL,
                              related_name="active_practices",
                              blank=True, null=True)
    model_portfolios = models.ManyToManyField(Portfolio,
                                              related_name="active_practices",
                                              blank=True)
    AFSL = models.ForeignKey(AFSL,
                             on_delete=models.SET_NULL,
                             related_name="active_practices",
                             blank=True, null=True)

    add_staff = models.CharField(max_length=100, blank=True, null=True)
    # This field is a hack - it would be better to handle removal of staff
    # through a custom update() method in the Practice serializer, but that
    # requires a fair bit of refactoring that I don't want to do at the moment.
    remove_staff = models.CharField(max_length=100, blank=True, null=True)


class User(AbstractUser):

    """User model. Customised to sub username with email"""

    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    AFSL = models.ForeignKey(AFSL,
                             related_name="authorised_reps",
                             on_delete=models.SET_NULL,
                             null=True, blank=True)
    AFSL_approved = models.BooleanField(default=False)
    linked_ARN = models.IntegerField(blank=True, null=True)

    active_rp = models.ForeignKey(RiskProfileGroup,
                                  on_delete=models.SET_NULL,
                                  related_name="active_users",
                                  null=True, blank=True)
    active_practice = models.ForeignKey(Practice,
                                        on_delete=models.SET_NULL,
                                        related_name="active_staff",
                                        null=True, blank=True)
    active_theme = models.ForeignKey(Theme,
                                     on_delete=models.SET_NULL,
                                     related_name="active_users",
                                     null=True, blank=True)

    practices = models.ManyToManyField(Practice,
                                       related_name="staff",
                                       blank=True)
    admin_practices = models.ManyToManyField(Practice,
                                             related_name="admins",
                                             blank=True)
    pending_practices = models.ManyToManyField(Practice,
                                               related_name="pending_staff",
                                               blank=True)

    verify_token = models.CharField(max_length=200, blank=True, null=True)
    verify_token_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return None

    @property
    def active_rp_name(self):
        if self.active_rp:
            if not self.active_rp.template and self.active_rp.default:
                return self.active_rp.unique_name
            else:
                return self.active_rp.name
        else:
            return None

    def __str__(self):
        return self.email


class Notification(models.Model):
    '''
    Used to manage the basic notifications that can be sent to users by the
    backend system on certain events.
    '''
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    practice = models.ForeignKey(Practice,
                                 on_delete=models.CASCADE,
                                 related_name="notifications",
                                 null=True, blank=True)
    target = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="notifications",
                               null=True, blank=True)
    # This field is used to store plaintext emails. Will store notifications
    # for individuals who do not yet have an account. On account creation,
    # we can check if that email has notifications waiting for them in the
    # backend and assign a real "target".
    to = models.CharField(max_length=100, blank=True, null=True)
