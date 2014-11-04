from django.conf.urls import url
from .views import *

urlpatterns = [  # Genereal urls
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^error/$', ErrorView.as_view(), name='error'),
    url(r'^result/$', ResultView.as_view(), name='result'),

    url(r'^device/(?P<device_id>\d+)/$', DeviceView.as_view(), name='device'),
]

#Scrud urls
scruds = [
    ['user', UserView],
    ['group', GroupView]
]

for scrud, ScrudView in scruds:
    urlpatterns.append(url(r'^' + scrud + '/all/$',
                           ScrudView.as_view(show_all='true'), name=scrud + '_all'))
    urlpatterns.append(url(r'^' + scrud + '/$',
                           ScrudView.as_view(), name=scrud))
    urlpatterns.append(url(r'^' + scrud + '/(?P<' + scrud + '_id>\d+)/$',
                           ScrudView.as_view(), name=scrud))
    urlpatterns.append(url(r'^' + scrud + '/delete/(?P<' + scrud + '_id>\d+)/$',
                           ScrudView.as_view(deactivate='true'), name=scrud + '_deactivate'))