from django.forms import ModelForm, NumberInput
from .models import Poll, Question, Answer


class PollModelForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']


class QuestionModelForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type', 'size']
        widgets = {
            'size': NumberInput(attrs={'min': 1, 'max': 10})
        }


class AnswerModelForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'max_value', 'min_value']
