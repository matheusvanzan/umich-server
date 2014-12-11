# -*- coding: utf-8 -*-
from .LoggedView import LoggedView
from django.shortcuts import render, get_object_or_404
from ..models import Device, SiteHistory


class DeviceView(LoggedView):
    template = 'device.html'
    device_id = 0
    device = Device()

    def dispatch(self, request, *args, **kwargs):
        print(str(kwargs))
        if 'device_id' in kwargs:
            self.device_id = kwargs['device_id']

            self.device = get_object_or_404(Device, pk=self.device_id)

        return super(DeviceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        super(DeviceView, self).get(request, *args, **kwargs)

        urls = []
        quants = []

        row = SiteHistory().getHistory(self.device)
        for url, quant in row:
            urls.append(url)
            quants.append(quant)

        self.data.update({'device': self.device})
        self.data.update({'urls': urls})
        self.data.update({'quants': quants})

        return render(request, self.template, self.data)