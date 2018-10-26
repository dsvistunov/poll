from django.conf.urls import url
from .views import PollCreateView, PollDetailView, PollUpdateView


urlpatterns = [
    url(r'^update/(?P<pk>[0-9]+)/$', PollUpdateView.as_view(), name='poll_update'),
    url(r'^detail/(?P<pk>[0-9]+)/$', PollDetailView.as_view(), name='poll_detail'),
    url(r'^create/$', PollCreateView.as_view(), name='poll_create'),
]
