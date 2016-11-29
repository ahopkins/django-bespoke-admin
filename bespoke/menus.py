from django.urls import reverse

class BaseMenu(object):
    def format_name(self, name):
        return name.replace('[-_]',' ')

    def make_link(self, page):
        name, title = page
        return "<a href='{url}'>{title}</a>".format(url=reverse(name), title=title)

    def render(self):
        return " | ".join([self.make_link(x) for x in self.pages])

class Menu(BaseMenu):
    pages = [('admin:commands-list', 'Commands')]