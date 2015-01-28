from django.db import models
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.utils.translation import ugettext


class Project(models.Model):
    """
    Model for projects
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def leave(self, user):
        """
        removes the given user from the project
        deletes the project if no user remains in the project
        :param user: the user who should be removed
        :return:
        """
        self.members.remove(user)

        # TODO: besprechen ob wir das so wollen
        if self.members.count() == 0:
            if not Invitation.objects.filter(project=self):
                self.delete()
                return

        self.save()


class ProjectForm(ModelForm):
    """
    Form for the project model
    """
    class Meta:
        model = Project
        fields = ('name', 'description')
        widgets = {
            'description': Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'name': ugettext('Name'),
            'description': ugettext('Description')
        }
        error_messages = {
            'name': {
                'max_length': ugettext('The name of the project is too long.')
            }
        }


class Invitation(models.Model):
    """
    Model for invitations
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    def accept(self):
        """
        accepts the invitation, adds the user to the project and deletes the invitation
        :return:
        """
        project = Project.objects.get(id=self.project.id)
        user = User.objects.get(id=self.user.id)
        project.members.add(user)
        project.save()
        self.delete()

    def reject(self):
        """
        deletes the invitation
        :return:
        """
        self.delete()

    @classmethod
    def get_for_user(cls, user):
        """
        creates a list of all invitations of a given user
        :param user: the user for which invitations are looked for
        :return: the list of invitations
        """
        return cls.objects.filter(user__id=user.id)

    def __str__(self):
        return self.user.username + " invited to " + self.project.name