# -*- coding: utf-8 -*-
from .LoggedView import LoggedView
from django.shortcuts import render
from ..models import Device


class IndexView(LoggedView):
    template = 'index.html'

    def get(self, request, *args, **kwargs):
        super(IndexView, self).get(request, *args, **kwargs)

        devices = Device.objects.all()

        self.data.update({'devices': devices})

        return render(request, self.template, self.data)