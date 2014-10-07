from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render


class MyView(View):
    template = ''
    master = 'master.html'
    master_scrud = 'scrud.html'
    redirect_results = reverse_lazy('result')
    redirect_login = reverse_lazy('login')
    redirect_error = reverse_lazy('error')
    data = {}

    def dispatch(self, request, *args, **kwargs):
        self.clear_data(request)
        return super(MyView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.clear_data(request)
        return render(request, self.template, self.data)

    def post(self, request, *args, **kwargs):
        self.clear_data(request)
        return render(request, self.template, self.data)

    def clear_data(self, request):
        self.data.clear()
        self.data.update({'master': self.master})
        self.data.update({'master_scrud': self.master_scrud})
        if request.user:
            self.data.update({'user': request.user})