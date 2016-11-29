from django.contrib import admin

from .urls import urlpatterns

def get_admin_urls(urls):
    def get_urls():
        return urlpatterns + urls
    return get_urls

admin.site.get_urls = get_admin_urls(admin.site.urls[0])