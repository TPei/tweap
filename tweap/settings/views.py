from django.shortcuts import render
from django.views.generic import View
from project_management.models import Project
from notification_center.models import NotificationEvent

class Settings(View):

    def get(self, request):
        user = request.user

        projects = Project.objects.filter(members=user)
        event_types = NotificationEvent.objects.all()
        context = {'projects': projects, 'event_types': event_types}
        return render(request, 'settings/settings.html', context)