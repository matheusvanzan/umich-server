# -*- coding: utf-8 -*-
from .LoggedView import LoggedView
from django.shortcuts import render
from ..models import Device


class IndexView(LoggedView):
    template = 'index.html'

    def get(self, request, *args, **kwargs):
        super(IndexView, self).get(request, *args, **kwargs)

        # CIRCLE and LIST view information
        devices = Device().getAllDevices()
        firstDevice = Device().getFirstDevice()
        otherDevices = Device().getOtherDevices()
        total = Device().getQuantDevices()

        self.data.update({'devices': devices})
        self.data.update({'firstDevice': firstDevice})
        self.data.update({'otherDevices': otherDevices})
        self.data.update({'total': total})

        return render(request, self.template, self.data)