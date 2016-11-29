from django import template
from django.utils.safestring import mark_safe


from bespoke.menus import Menu

register = template.Library()

@register.simple_tag
def bespoke_menu():
    return mark_safe(Menu().render())