from django import forms
from .models import Scrud, User, Group


class ScrudForm(forms.ModelForm):
    class Meta:
        model = Scrud


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'groups',
                  'user_permissions', 'is_staff',
                  'is_active', 'is_superuser',
                  'last_login', 'date_joined']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['groups'].label = "Grupos (*Ctrl)"


class UserSimpleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'groups']

    def __init__(self, *args, **kwargs):
        super(UserSimpleForm, self).__init__(*args, **kwargs)
        self.fields['groups'].label = "Grupos (*Ctrl)"


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group