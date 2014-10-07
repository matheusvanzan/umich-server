from .MyView import MyView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.shortcuts import render
from django.http import HttpResponseRedirect


class LoginView(MyView):
    template = 'login.html'
    redirect = reverse_lazy('index')
    username = ''
    password = ''
    data = {}

    def get(self, request, *args, **kwargs):
        super(LoginView, self).get(request, *args, **kwargs)
        form = AuthenticationForm()
        self.data.update({'form': form})
        return render(request, self.template, self.data)

    def post(self, request, *args, **kwargs):
        super(LoginView, self).post(request, *args, **kwargs)
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