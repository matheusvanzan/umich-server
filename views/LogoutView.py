from .MyView import MyView
from django.contrib.auth import logout as django_logout
from django.shortcuts import render


class LogoutView(MyView):
    template = 'login.html'
    data = {}

    def get(self, request, *args, **kwargs):
        super(LogoutView, self).get(request, *args, **kwargs)
        django_logout(request)
        return render(request, self.template)