# -*- coding: utf-8 -*-
from .LoggedView import LoggedView
from django.shortcuts import render
from ..models import Device


class IndexView(LoggedView):
    template = 'index.html'

    def get(self, request, *args, **kwargs):
        super(IndexView, self).get(request, *args, **kwargs)

        # CIRCLE and LIST view information
        devices = Device.objects.order_by('type')
        self.data.update({'devices': devices})

        # MAP view information
        modems = Device.objects.filter(type='0_modem')
        routers = Device.objects.filter(type='1_router')

        self.firstDevice = Device()
        if len(modems) != 0:
            self.firstDevice = modems[0]
        elif len(routers) != 0:
            self.firstDevice = routers[0]
        else:
            self.firstDevice = devices[0]

        self.data.update({'firstDevice': self.firstDevice})

        return render(request, self.template, self.data)