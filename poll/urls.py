from django.conf.urls import url
from .views import (
    PollCreateView,
    PollDetailView,
    PollUpdateView,
    QuestionCreateView
)


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', PollUpdateView.as_view(), name='poll_update'),
    url(r'^(?P<pk>\d+)/questions/$', QuestionCreateView.as_view(), name='question_create'),
    url(r'^detail/(?P<pk>\d+)/$', PollDetailView.as_view(), name='poll_detail'),
    url(r'^create/$', PollCreateView.as_view(), name='poll_create'),
]
