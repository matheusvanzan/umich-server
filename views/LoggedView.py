from .MyView import MyView
from django.shortcuts import redirect


class LoggedView(MyView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(self.redirect_login + '?next=' + request.path)
        else:
            self.data.update({'user': request.user})
            return super(LoggedView, self).dispatch(request, *args, **kwargs)