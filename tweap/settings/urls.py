from django.conf.urls import patterns, url
from settings import views

urlpatterns = patterns(
    '',
    url(r'^$', views.Settings.as_view(), name='settings'),
)
