from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index, name='Index'),
    url(r'^position/$',views.position_info, name='position_info'),
    url(r'^info/$', views.reload_info),
    url(r'^trade/$', views.change_state),
    ]
