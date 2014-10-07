# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .ScrudView import ScrudView
from ..models import User
from ..forms import UserForm, UserSimpleForm


class UserView(ScrudView):  # Inherits but it's so specific that
    scrud_string = 'user'   # it overrides almost every method
    scrud_object = User
    scrud_form = UserForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            self.scrud_form = UserSimpleForm
        return super(UserView, self).dispatch(request, *args, **kwargs)

    def scrud_all(self, request):
        print('inside scrud_all')
        scruds = self.scrud_object.objects.all()
        scruds_return = []
        for scrud in scruds:
            if request.user.is_superuser:
                scruds_return.append(scrud)
            else:
                if scrud.is_superuser:
                    pass
                else:
                    scruds_return.append(scrud)
        self.data.update({self.scrud_string + 's': scruds_return,
                          'show_all': self.show_all})
        return render(request, self.template, self.data)

    def scrud_retrieve(self, request):
        scrud = get_object_or_404(self.scrud_object, pk=self.scrud_id)
        if (not request.user.is_superuser) and scrud.is_superuser:
            return HttpResponseRedirect(self.redirect_error)
        return super(UserView, self).scrud_retrieve(request)

    def scrud_create(self, request):
        print('inside scrud_create')
        form = self.scrud_form(request.POST)
        if form.is_valid():
            if User.has_equal(form):
                self.data.update({'form': form})
                self.data.update({'error_message': 'Usuário já existe!'})
                return render(request, self.template, self.data)
            else:
                new_user = User.objects.create_user(form.cleaned_data['username'],
                                                    form.cleaned_data['email'],
                                                    form.cleaned_data['password'])
                self.save_user(request, new_user, form)
            return HttpResponseRedirect(self.redirect_results)
        else:
            self.data.update({'form': form})
            return render(request, self.template, self.data)

    def scrud_update(self, request):
        print('inside scrud_update')
        user = get_object_or_404(User, pk=self.scrud_id)
        form = self.scrud_form(request.POST, instance=user)
        if form.is_valid():
            print('valid form')
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            self.save_user(request, user, form)
            return HttpResponseRedirect(self.redirect_results)
        else:
            print('not valid form')
            self.data.update({'form': form})
            self.data.update({'error_message': 'Erro no preenchimento do formulário!'})
            return render(request, self.template, self.data)

    @staticmethod
    def save_user(request, user, form):
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.groups = form.cleaned_data['groups']

        if request.user.is_superuser:
            user.user_permissions = form.cleaned_data['user_permissions']
            user.is_staff = form.cleaned_data['is_staff']
            user.is_active = form.cleaned_data['is_active']
            user.is_superuser = form.cleaned_data['is_superuser']
            user.last_login = form.cleaned_data['last_login']
            user.date_joined = form.cleaned_data['date_joined']

        user.save()