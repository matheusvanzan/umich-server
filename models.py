from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup


class Scrud(models.Model):
    #data = models.CharField(max_length=200)

    @staticmethod
    def has_equal(scrud=None, form=None):
        return False
        # scruds = Scrud.objects.all()
        # for s in scruds:
        #     if scrud and s.data == scrud.data:
        #         return True
        #     if form and s.data == form.cleaned_data['data']:
        #         return True
        # return False

    def deactivate(self):
        pass


class User(DjangoUser):

    @staticmethod
    def has_equal(scrud=None, form=None):
        return False
        # scruds = Scrud.objects.all()
        # for s in scruds:
        #     if scrud and s.data == scrud.data:
        #         return True
        #     if form and s.data == form.cleaned_data['data']:
        #         return True
        # return False

    def is_login_admin(self):
        pass

    def deactivate(self):
        pass


class Group(DjangoGroup):
    def deactivate(self):
        pass


        # class Note(models.Model):
        # title = models.CharField(max_length=200)
        # body = models.CharField(max_length=1000)
        # 	date_created = DateTimeField(auto_now_add=True)
        # 	date_last_edited = DateTimeField(auto_now=True)
        #
        # 	def __str__(self):
        # 		return self.title + ': ' + self.body