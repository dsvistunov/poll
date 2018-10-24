from django.conf.urls import url
from .views import PollView


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', PollView.as_view(), name='poll_detail'),
]
