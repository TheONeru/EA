from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.account_info, name='account_info'),
    url(r'^position/$',views.position_info, name='position_info'),
    ]
