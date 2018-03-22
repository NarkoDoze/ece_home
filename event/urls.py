from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'event/(?P<idx>[-\w]+)', views.event_content, name='event_content'),
    url(r'event', views.event_home, name='event_home'),
]
