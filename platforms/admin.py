from django.contrib import admin
from platforms.models import Platform, PlatformFamilyGroups, PlatformNames

# Register your models here.
admin.site.register(Platform)
admin.site.register(PlatformNames)
admin.site.register(PlatformFamilyGroups)
