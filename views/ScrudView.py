from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .LoggedView import LoggedView
from ..models import Scrud
from ..forms import ScrudForm


# SCRUD - Search, Create, Retrieve, Update, Delete
class ScrudView(LoggedView):
    scrud_string = 'scrud'
    scrud_object = Scrud
    scrud_form = ScrudForm

    show_all = 'false'
    deactivate = 'false'
    scrud_id = 0
     
    fields = {}
    last_saved = None

    def __init__(self, *args, **kwargs):
        print('inside init')
        super(ScrudView, self).__init__(*args, **kwargs)
        self.scrud_id_string = self.scrud_string + '_id'
        self.template = self.scrud_string + '.html'
        self.data.update({'show_all': 'false'})
        self.data.update({'deactivate': 'false'})

    def dispatch(self, request, *args, **kwargs):
        print('inside dispatch')
        if self.scrud_id_string in kwargs:
            print('scrud_id in kwargs')
            print(str(kwargs))
            self.scrud_id = kwargs[self.scrud_id_string]
            self.data.update({self.scrud_id_string: self.scrud_id})
        return super(ScrudView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        super(ScrudView, self).get(request, *args, **kwargs)
        print('inside get')
        if self.show_all == 'true':
            print('show_all = true')
            return self.scrud_all(request)
        elif self.deactivate == 'true':
            print('deactivate = true')
            return self.scrud_deactivate(request)
        else:
            print('show_all = false and delete = false')
            if self.scrud_id == 0:
                print('scrud_id = 0')
                return self.scrud_new(request)
            else:
                print('scrud_id != 0')
                return self.scrud_retrieve(request)

    def post(self, request, *args, **kwargs):
        super(ScrudView, self).post(request, *args, **kwargs)
        print('inside post')
        if self.scrud_id == 0:
            return self.scrud_create(request)
        else:
            return self.scrud_update(request)

    def scrud_all(self, request):
        print('inside scrud_all')
        scruds = self.scrud_object.objects.all()
        self.data.update({self.scrud_string + 's': scruds})
        self.data.update({'show_all': self.show_all})
        return render(request, self.template, self.data)

    def scrud_new(self, request):
        print('inside scrud_new')
        form = self.scrud_form(self.fields)
        self.data.update({'form': form})
        return render(request, self.template, self.data)

    def scrud_retrieve(self, request):
        print('inside scrud_retrieve')
        scrud = get_object_or_404(self.scrud_object, pk=self.scrud_id)
        form = self.scrud_form(instance=scrud)
        self.data.update({'form': form})
        self.data.update({self.scrud_id_string: self.scrud_id})
        return render(request, self.template, self.data)

    def scrud_create(self, request):
        print('inside scrud_create')
        form = self.scrud_form(request.POST)
        if form.is_valid():
            if self.scrud_object.has_equal(form=form):
                self.data.update({'form': form})
                self.data.update({'error_message': self.scrud_string + ' already exists!'})
                return render(request, self.template, self.data)
            else:
                self.last_saved = form.save()
                return HttpResponseRedirect(self.redirect_results)
        else:
            self.data.update({'form': form,
                              'error_message': 'Error filling form!'})
            return render(request, self.template, self.data)

    def scrud_update(self, request):
        print('inside scrud_update')
        scrud = get_object_or_404(self.scrud_object, pk=self.scrud_id)
        form = self.scrud_form(request.POST, instance=scrud)
        if form.is_valid():
            self.last_saved = form.save()
            return HttpResponseRedirect(self.redirect_results)
        else:
            self.data.update({'form': form})
            return render(request, self.template, self.data)

    def scrud_deactivate(self, request):
        if request.user.is_superuser:
            scrud = get_object_or_404(self.scrud_object, pk=self.scrud_id)
            scrud.delete()
            return HttpResponseRedirect(self.redirect_results)
        else:
            return HttpResponseRedirect(self.redirect_error)