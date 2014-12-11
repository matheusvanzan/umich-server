from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup
from django.templatetags.static import static
from datetime import datetime, timezone
import math
from django.db import connection


class Scrud(models.Model):
    # data = models.CharField(max_length=200)

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

    def deactivate(self):
        pass


class User(DjangoUser):
    @staticmethod
    def has_equal(scrud=None, form=None):
        return False
        # scruds = Scrud.objects.all()
        # for s in scruds:
        # if scrud and s.data == scrud.data:
        # return True
        #     if form and s.data == form.cleaned_data['data']:
        #         return True
        # return False

    def is_login_admin(self):
        pass

    def deactivate(self):
        pass


class Group(DjangoGroup):
    @staticmethod

    def has_equal(scrud=None, form=None):
        return False
        # scruds = Scrud.objects.all()
        # for s in scruds:
        # if scrud and s.data == scrud.data:
        # return True
        #     if form and s.data == form.cleaned_data['data']:
        #         return True
        # return False

    def deactivate(self):
        pass  # ### Specific application models

DEVICE_TYPES = (
    ('0_modem', 'Modem'),
    ('1_router', 'Router'),
    ('2_switch', 'Switch'),
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
        self.onOff = ''
        if self.isOnline():
            self.onOff = 'on'
        else:
            self.onOff = 'off'

        url = 'images/' + str(self.type) + '_' + self.onOff + '.png'
        return static(url)

    def isOn(self):
        delta = datetime.now(timezone.utc) - self.lastOn
        deltaSecs = delta.total_seconds() - 5 * 60 * 60  # timezone problems
        return deltaSecs < 300  # 5 minutes

    def isOnline(self):
        delta = datetime.now(timezone.utc) - self.lastOnline
        deltaSecs = delta.total_seconds() - 5 * 60 * 60  # timezone problems
        return deltaSecs < 300  # 5 minutes

    def getQuantDevices(self):
        return len(Device.objects.all())

    def getFirstDevice(self):
        return Device.objects.raw('''SELECT * FROM myproject_device
                                    WHERE id NOT IN (
                                       SELECT device2_id FROM myproject_deviceconnection
                                    )
                                    ORDER BY type;''')[0]

    def getParentDevice(self):
        return Device.objects.raw('''SELECT * FROM myproject_device
                                    WHERE id IN (
                                        SELECT device1_id FROM myproject_deviceconnection WHERE device2_id = %s
                                    )
                                    ORDER BY type;''', [self.id])[0]

    def getAllDevices(self):
        return Device.objects.raw('''SELECT * FROM myproject_device
                                    WHERE id NOT IN (
                                       SELECT device2_id FROM myproject_deviceconnection
                                    )
                                     UNION
                                    SELECT * FROM myproject_device
                                    WHERE id IN (
                                       SELECT device2_id FROM myproject_deviceconnection
                                    )
                                    ORDER BY type;''')

    def getOtherDevices(self):
        return Device.objects.raw('''SELECT * FROM myproject_device
                                    WHERE id IN (
                                       SELECT device2_id FROM myproject_deviceconnection
                                    )
                                    ORDER BY type;''')

    def getChildDevices(self):
        return Device.objects.raw('''SELECT * FROM myproject_device
                                     WHERE id IN (
                                        SELECT device2_id
                                        FROM myproject_device a INNER JOIN myproject_deviceconnection b ON a.id = b.device1_id
                                        WHERE a.id = %s
                                    )
                                    ORDER BY type;''', [self.id])


    # Get device level
    def getLevel(self):
        parentDevice = self
        count = 0
        while parentDevice != self.getFirstDevice():
            parentDevice = parentDevice.getParentDevice()
            count += 1
        return count

    # Get the biggest level
    def getMaxLevel(self):
        maxLevel = 0
        for device in Device.objects.all():
            if maxLevel < device.getLevel():
                maxLevel = device.getLevel()
        return maxLevel

    # Get number of devices in some level
    # def getQuantLevel(self):
    #     quant = 0
    #     for device in Device.objects.all():
    #         if device.getLevel() == self.getLevel():
    #             quant += 1
    #     return quant

    # Get unit teta for some level
    def getUnitTeta(self):
        if self.getLevel() == 0:
            return 2 * math.pi
        else:
            #return self.getParentDevice().getUnitTeta() / (self.getQuantLevel() + 1)
            return self.getParentDevice().getUnitTeta() / len(list(self.getParentDevice().getChildDevices()))

    # Get device number in order of level (just inside its parents space)
    def getNumberInLevel(self):
        number = 0
        if self.getLevel() == 0:
            return 0
        else:
            for device in self.getParentDevice().getChildDevices():
                if device == self:
                    return number
                else:
                    number += 1
            return 0

    def getTeta(self):
        if self.getLevel() == 0:
            return 0
        elif self.getLevel() == 1:
            return self.getUnitTeta() * self.getNumberInLevel() + self.getUnitTeta() / 2
        else:
            offset = self.getParentDevice().getTeta() - (self.getParentDevice().getUnitTeta() / 2)
            #return offset + self.getUnitTeta() * (self.getNumberInLevel() + 1)
            return offset + self.getUnitTeta() * self.getNumberInLevel() + self.getUnitTeta() / 2


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

    def getHistory(self, device):
        cursor = connection.cursor()

        cursor.execute('''SELECT url, COUNT(id)
                          FROM myproject_sitehistory
                          WHERE device_id=%s
                          GROUP BY url;''', [device.id])
        row = cursor.fetchall()

        return row