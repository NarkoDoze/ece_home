from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'announce/(?P<idx>[-\w]+)', views.announce_content, name='announce_content'),
    url(r'announce', views.announce_home, name='announce_home'),
]