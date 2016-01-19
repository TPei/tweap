from django.db import models
from django.contrib.auth.models import User
from project_management.models import Project
from notification_center.models import NotificationEvent


class NotificationSetting(models.Model):
    event = models.ForeignKey(NotificationEvent, null=False)
    setting = models.CharField(max_length=50, null=False) # email, dashboard, multiple
    user = models.ForeignKey(User, null=False)


class ProjectOrder(models.Model):
    project = models.ForeignKey(Project, null=False)
    user = models.ForeignKey(User, null=False)
    order_number = models.IntegerField(null=False)


class LanguagePreference(models.Model):
    primary_language = models.CharField(max_length=20, null=False)
    user = models.ForeignKey(User, null=False)