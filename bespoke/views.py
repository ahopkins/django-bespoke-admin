from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib import admin
from django.apps import apps
from django.core.management import find_commands, call_command
from django.conf import settings
from django.utils import timezone

import os, sys

def bespoke(request):
    def get_commands(app):
        app_config = apps.get_app_config(app.get('app_label'))
        return find_commands(os.path.join(app_config.path, 'management'))

    site = admin.site
    app_list = site.get_app_list(request)

    app_list = [dict(app, commands=get_commands(app)) for app in app_list]

    context = dict(site.each_context(request),
                   title=_("Management Commands"),
                   app_list=app_list)
    return render(request, 'bespoke/index.html', context)

def run_command(request, app_name, command):
    sysout = sys.stdout

    
    response = HttpResponse()
    sys.stdout = response
    call_command(command)
    sys.stdout = sysout

    file_name = os.path.join(settings.BASE_DIR, 'logs', 'bespoke-admin-{}.log'.format(app_name))
    with open(file_name, 'a') as file:
        file.write("[{}] {}".format(str(timezone.now()), response.content.decode('utf-8')))
    
    site = admin.site
    context = dict(site.each_context(request),
                   title=_("History"),
                   command=command,
                   app_name=app_name,
                   content=response.content)
    return render(request, 'bespoke/run.html', context)


def run_history(request, app_name, command):
    def pad_spacing(line):
        if line.startswith('['):
            return line
        return ''.join([' ' for _ in range(35)]) + line
    file_name = os.path.join(settings.BASE_DIR, 'logs', 'bespoke-admin-{}.log'.format(app_name))
    with open(file_name, 'r') as file:
        contents = file.readlines()
    contents = ''.join([pad_spacing(line) for line in contents])

    site = admin.site
    context = dict(site.each_context(request),
                   title=_("History"),
                   command=command,
                   app_name=app_name,
                   contents=contents)
    return render(request, 'bespoke/history.html', context)