import json

from django.http import JsonResponse, Http404
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Poll, Question, Answer, UserAgent
from .forms import PollModelForm, QuestionModelForm, AnswerModelForm


class JSONResponseMixin:

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            context,
            safe=False,
            **response_kwargs
        )

    # def get_context_data(self, **kwargs):
    #     context = {}
    #     question = self.object
    #     context['question'] = {'id': question.id, 'text': question.text}
    #     context['choices'] = []
    #     for choise in question.answer_set.all():
    #         context['choices'].append({
    #             "id": choise.id, "type": choise.type,
    #             "text": choise.text, "votes": choise.votes
    #         })
    #     return context

    def is_data_valid(self, request):
        data = json.loads(request.body)
        question = data.get('question', None)
        choices = data.get('choices', None)
        permission = data.get('permission', None)
        errors = {
            'errors': []
        }
        if question is None:
            errors['errors'].append({'message': 'key "question" not in request body'})
        elif choices is None:
            errors['errors'].append({'message': 'key "errors" not in request body'})
        elif not isinstance(choices, list):
            errors['errors'].append({'message': 'key "choices" must be list type'})
        elif len(choices) == 0:
            errors['errors'].append({'message': 'choices is empty list'})
        elif permission is None:
            errors['errors'].append({'message': 'key "permissions" not in request body'})
        elif permission == '':
            errors['errors'].append({'message': 'permissions is empty'})
        elif permission not in ['not_authorized', 'authorized', 'email_confirmed']:
            errors['errors'].append({
                'message': 'passed "%s" permission, but allowed is: '
                           'not_authorized, authorized, email_confirmed' % permission})

        if errors['errors']:
            self.errors = errors
            return False
        else:
            self.question = question
            self.choices = choices
            self.permission = permission
            return True


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
        type_ = request.POST.get('type', None)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.poll_id = self.kwargs.get(self.pk_url_kwarg)
            self.object.save()
        else:
            for key, value in form.errors.as_data().items():
                errors[key] = value[0].message

        for key, value in request.POST.items():
            if 'choice' in key:
                answer_form = AnswerModelForm({'type': type_, 'text': value})
                if answer_form.is_valid():
                    answer = answer_form.save(commit=False)
                    answer.question = self.object
                    answer.save()
                else:
                    for _, value in answer_form.errors.as_data().items():
                        errors[key] = value[0].message

        if errors:
            return self.render_to_json_response(errors, status=400)
        else:
            return self.render_to_json_response({'msg': 'success'})

    # def get(self, request, *args, **kwargs):
    #     return self.render_to_response({'errors': 'Method Get not allowed'}, status=405)
    #
    # def post(self, request, *args, **kwargs):
    #     if self.is_data_valid(request):
    #         question = Question.objects.create(text=self.question)
    #         for choice in self.choices:
    #             question.answer_set.create(type=choice['type'], text=choice['text'])
    #
    #         content_type = ContentType.objects.get_for_model(Question)
    #         Permission.objects.create(
    #             codename=self.permission,
    #             content_type=content_type
    #         )
    #
    #         self.object = question
    #         return self.render_to_response(self.get_context_data(), status=200)
    #     else:
    #         return self.render_to_response(self.errors, status=400)
    #
    # def render_to_response(self, context, **response_kwargs):
    #     return self.render_to_json_response(context, **response_kwargs)


class PollDetailView(JSONResponseMixin, DetailView):
    model = Question

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            context = self.get_context_data()
            return self.render_to_response(context, status=200)
        else:
            error = 'Object with id = %s, does not exist' % self.kwargs.get(self.pk_url_kwarg)
            context = {'errors': {'message': error}}
            return self.render_to_response(context, status=404)

    def get_object(self, queryset=None):
        try:
            obj = super(PollDetailView, self).get_object()
        except Http404:
            obj = None
        return obj

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class PollUpdateView(JSONResponseMixin, UpdateView):
    model = Question

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            if self.is_data_valid(request):
                question = self.object
                if question.text != self.question:
                    question.text = self.question
                    question.save()
                for choice in self.choices:
                    try:
                        answer = question.answer_set.get(id=choice['id'])
                        if answer.type != choice['type']:
                            answer.type = choice['type']
                        elif answer.text != choice['text']:
                            answer.text = choice['text']
                        elif answer.votes != choice['votes']:
                            answer.votes += 1
                        answer.save()
                    except KeyError:
                        Answer.objects.create(question=question, text=choice['text'], type=choice['type'])

                UserAgent.objects.create(date=request.META['HTTP_USER_AGENT'])

                return self.render_to_response(self.get_context_data(), status=200)
            else:
                return self.render_to_response(self.errors, status=400)
        else:
            error = 'Object with id = %s, does not exist' % self.kwargs.get(self.pk_url_kwarg)
            context = {'errors': {'message': error}}
            return self.render_to_response(context, status=404)

    def get_object(self, queryset=None):
        try:
            obj = super(PollUpdateView, self).get_object()
        except Http404:
            obj = None
        return obj

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
