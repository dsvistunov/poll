from django.forms import ModelForm
from .models import Poll, Question, Answer


class PollModelForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']


class QuestionModelForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AnswerModelForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['type', 'text']
