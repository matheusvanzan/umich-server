from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup
from django.templatetags.static import static


class Scrud(models.Model):
    # data = models.CharField(max_length=200)

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
        # if scrud and s.data == scrud.data:
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


# ### Specific application models

DEVICE_TYPES = (
    ('0_modem', 'Modem'),
    ('1_router', 'Router'),
    ('2_hub', 'Hub'),
    ('3_pc', 'Computer'),
    ('4_printer', 'Printer'),
    ('5_phone', 'Cellphone')
)


class Device(models.Model):
    type = models.CharField(choices=DEVICE_TYPES, max_length=100)
    name = models.CharField(max_length=100)
    lastOn = models.DateTimeField()
    lastOnline = models.DateTimeField()
    ipAddress = models.CharField(max_length=100)
    macAddress = models.CharField(max_length=100)
    opSystem = models.CharField(max_length=100)
    isWireless = models.BooleanField()

    @property
    def getImage(self):
        onOff = ''
        if self.isOnline():
            onOff = 'on'
        else:
            onOff = 'off'
        return static('images/' + self.type + '_' + onOff + '.png')

    def isOn(self):
        return True

    def isOnline(self):
        return True

    def getConnectedDevices(self):
        returnDevices = []
        cons = DeviceConnection.objects.all()
        for con in cons:
            if self == con.device1:
                returnDevices.append(con.device2)
            if self == con.device2:
                returnDevices.append(con.device1)
        return returnDevices

    def __str__(self):
        return self.name + ' - ' + self.ipAddress


class DeviceConnection(models.Model):
    device1 = models.ForeignKey(Device, related_name='Device 1')
    device2 = models.ForeignKey(Device, related_name='Device 2')


class SiteHistory(models.Model):
    device = models.ForeignKey(Device)
    timestamp = models.DateTimeField()
    url = models.URLField()
    band = models.FloatField()