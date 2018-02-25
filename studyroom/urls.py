from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'studyroom/check', views.sroom_chk, name='sroom_chk'),
    url(r'studyroom/(?P<idx>[-\w]+)', views.sroom_rsv, name='sroom'),
    url(r'studyroom', views.sroom_home, name='sroom_home'),
]