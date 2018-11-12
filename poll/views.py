from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Poll, Question, Answer, UserAgent, Anonymous
from .forms import PollModelForm, QuestionModelForm, AnswerModelForm


class JSONResponseMixin:

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            context,
            safe=False,
            **response_kwargs
        )


class PollCreateView(CreateView):
    model = Poll
    form_class = PollModelForm
    template_name = 'poll_create.html'


class QuestionCreateView(JSONResponseMixin, CreateView):
    model = Question
    form_class = QuestionModelForm
    template_name = 'question_create.html'
    success_url = '/create/'

    def post(self, request, *args, **kwargs):
        errors = {}
        form = self.get_form()
        try:
            with transaction.atomic():
                if form.is_valid():
                    self.object = form.save(commit=False)
                    self.object.poll_id = self.kwargs.get(self.pk_url_kwarg)
                    self.object.save()
                else:
                    for key, value in form.errors.as_data().items():
                        errors[key] = value[0].message

                for key, value in request.POST.items():
                    if 'choice' in key:
                        max_value = request.POST.get('max_value', None)
                        min_value = request.POST.get('min_value', None)
                        answer_form = AnswerModelForm({'text': value, 'max_value': max_value, 'min_value': min_value})
                        if answer_form.is_valid() and self.object:
                            answer = answer_form.save(commit=False)
                            answer.question = self.object
                            answer.save()
                        else:
                            for _, value in answer_form.errors.as_data().items():
                                errors[key] = value[0].message
                if errors:
                    raise ValidationError('')
                else:
                    return self.render_to_json_response({'msg': 'success'})
        except ValidationError:
            return self.render_to_json_response(errors, status=400)


class PollDetailView(DetailView):
    template_name = 'poll_detail.html'
    model = Poll


class PollUpdateView(JSONResponseMixin, UpdateView):
    model = Poll
    template_name = 'poll_update.html'
    form_class = PollModelForm
    template_name_suffix = 'poll'
    success_url = '/polls/'

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if 'question' in key and value:
                _, question_id = key.split('_')
                question = Question.objects.get(id=question_id)
                if request.user.is_authenticated():
                    user = request.user
                    if question.voted_users.filter(id=user.id).exists():
                        context = {'error': 'your answers cannot be accepted because you are already answered'}
                        return self.render_to_response(context=context)
                    else:
                        question.voted_users.add(user)
                else:
                    hash_ = request.POST.get('hashed_ip')
                    anonym, _ = Anonymous.objects.get_or_create(hash=hash_)
                    if question.voted_anonymous.filter(hash=hash_).exists():
                        context = {'error': 'your answers cannot be accepted because you are already answered'}
                        return self.render_to_response(context=context)
                    else:
                        question.voted_anonymous.add(anonym)

                if question.type == 'TXT' or question.type == 'NUM':
                    question.answer_set.create(text=value)
                else:
                    answer = question.answer_set.get(id=value)
                    answer.votes += 1
                    answer.save()
        self.object = self.get_object()
        return HttpResponseRedirect(self.object.get_detail_url())
