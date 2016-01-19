from django.db import models
from django.contrib.auth.models import User
from project_management.models import Project
from django.core.exceptions import ObjectDoesNotExist

class NotificationEvent(models.Model):
    text = models.CharField(max_length=50, null=False)
    # is shown in settings pane
    description = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.text


class Notification(models.Model):
    receiver = models.ForeignKey(User, null=False, related_name='%(class)s_receiver')
    trigger_user = models.ForeignKey(User, null=False, related_name='%(class)s_triggerer')
    timestamp = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, null=False)
    target_url = models.CharField(max_length=100, blank=False)
    event = models.ForeignKey(NotificationEvent, null=False)

    def __str__(self):
        return str(self.event) + ", from " + self.trigger_user.username + ", to " + self.receiver.username

    @classmethod
    def create(cls, receiver, trigger_user, project, target_url, event_string):
        """
        create a notification for a user
        :param receiver:
        :param trigger_user:
        :param project:
        :param target_url:
        :param event_string:
        :return:
        """
        if receiver == trigger_user:
            return

        try:
            event = NotificationEvent.objects.get(text=event_string)
        except ObjectDoesNotExist:
            event = NotificationEvent(text=event_string)
            event.save()

        cls(receiver=receiver, trigger_user=trigger_user, project=project, target_url=target_url, event=event).save()


    @classmethod
    def bulk_create(cls, username_list, trigger_user, project, target_url, event_string):
        """
        create a notification for a bunch of people
        :param username_list:
        :param trigger_user:
        :param project:
        :param target_url:
        :param event_string:
        :return:
        """
        for username in username_list:
            receiver = User.objects.get(username=username)
            cls.create(receiver, trigger_user, project, target_url, event_string)

    @classmethod
    def project_notification(cls, trigger_user, project, target_url, event_string):
        for receiver in project.members.all():
            cls.create(receiver, trigger_user, project, target_url, event_string)




