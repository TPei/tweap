from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponseRedirect

urlpatterns = patterns(
    '',
    url(r'^$', lambda r: HttpResponseRedirect('dashboard')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^users/', include('user_management.urls', namespace='user_management')),
    url(r'^projects/', include('project_management.urls', namespace='project_management')),
    url(r'^todo/', include('todo.urls', namespace='todo')),
    url(r'^calendar/', include('cal.urls', namespace='cal')),
    url(r'^notifications/', include('notification_center.urls', namespace='notification_center')),
    url(r'^chat/', include('chat.urls', namespace='chat')),
    url(r'^settings/', include('settings.urls', namespace='settings')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^rosetta/', include('rosetta.urls')),
    )

urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
