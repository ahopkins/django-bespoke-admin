from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^commands/(?P<app_name>[a-zA-Z0-9_]+)/(?P<command>[a-zA-Z0-9_]+)/history', admin.site.admin_view(views.run_history), name="run-history"),
    url(r'^commands/(?P<app_name>[a-zA-Z0-9_]+)/(?P<command>[a-zA-Z0-9_]+)', admin.site.admin_view(views.run_command), name="run-command"),
    url(r'^commands/$', admin.site.admin_view(views.bespoke), name="commands-list")
]