# -*- coding: utf-8 -*-
from .LoggedView import LoggedView


class IndexView(LoggedView):
    template = 'index.html'