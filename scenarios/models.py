import uuid
import os
from django.db import models
from django.conf import settings
from riskprofiles.models import RiskProfile
from documents.models import Theme
from django.utils import timezone


class Scenario(models.Model):

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="scenarios",
                             blank=True, null=True)
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           related_name="shared_scenarios",
                                           blank=True)
    client = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    risk_profile = models.ForeignKey(RiskProfile,
                                     on_delete=models.SET_NULL,
                                     related_name="scenarios",
                                     blank=True, null=True)

    practice = models.ForeignKey('users.Practice',
                                 on_delete=models.SET_NULL,
                                 related_name="scenarios",
                                 blank=True, null=True)
    theme = models.ForeignKey(Theme,
                              on_delete=models.SET_NULL,
                              related_name="scenarios",
                              blank=True, null=True)
    generate_document = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    @property
    def scenario_total(self):
        platforms = self.platforms.all()
        scenario_total = 0
        for platform in platforms:
            scenario_total += platform.platform_total
        return scenario_total

    @property
    def scenario_total_cur(self):
        platforms = self.platforms.filter(scenario=self,
                                          status="Current")
        scenario_total = 0
        for platform in platforms:
            scenario_total += platform.platform_total
        return scenario_total

    @property
    def scenario_total_rec(self):
        platforms = self.platforms.filter(scenario=self,
                                          status="Recommended")
        scenario_total = 0
        for platform in platforms:
            scenario_total += platform.platform_total
        return scenario_total

    @property
    def scenario_total_alt(self):
        platforms = self.platforms.filter(scenario=self,
                                          status="Alternative")
        scenario_total = 0
        for platform in platforms:
            scenario_total += platform.platform_total
        return scenario_total

    @property
    def risk_profile_group_name(self):
        if self.risk_profile:
            if not self.risk_profile.group.template and self.risk_profile.group.default:
                return self.risk_profile.group.unique_name
            else:
                return self.risk_profile.group.name


            return self.risk_profile.group.name
        else:
            return None



class Report(models.Model):

    scenario = models.ForeignKey(Scenario,
                                 on_delete=models.CASCADE)

    def upload_path(self, filename):
        file_path = os.path.join(settings.REPORTS_PATH, str(self.scenario.id), filename)
        return file_path

    file = models.FileField(upload_to=upload_path,
                            max_length=500,
                            blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['created_at']
