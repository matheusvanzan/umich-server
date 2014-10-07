from .MyView import MyView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate


class CheckLoginView(MyView):
    template = 'login.html'
    redirect = reverse_lazy('index')
    username = ''
    password = ''
    data = {}

    def post(self, request):
        self.username = request.POST['username']
        self.password = request.POST['password']
        user = authenticate(username=self.username, password=self.password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return HttpResponseRedirect(self.redirect)
            else:
                self.data.update({'error_message': "Conta desativada!"})
                return render(request, self.template, self.data)
        else:
            self.data.update({'error_message': "Verifique o login e a senha!"})
            return render(request, self.template, self.data)