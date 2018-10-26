import json
from django.http import JsonResponse, Http404
from django.views.generic import CreateView, DetailView, UpdateView
from .models import Question, Answer


class JSONResponseMixin:

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            context,
            safe=False,
            **response_kwargs
        )

    def get_context_data(self, **kwargs):
        context = {}
        question = self.object
        context['question'] = {'id': question.id, 'text': question.text}
        context['choices'] = []
        for choise in question.answer_set.all():
            context['choices'].append({"id": choise.id, "type": choise.type, "text": choise.text})
        return context

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_json_response(self.get_context_data())


class PollCreateView(JSONResponseMixin, CreateView):
    model = Question

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'errors': 'Method Get not allowed'}, status=405)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        question = data.get('question', None)
        choices = data.get('choices', None)
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

        if errors['errors']:
            return self.render_to_json_response(errors, status=400)
        else:
            question = Question.objects.create(text=question)
            for choice in choices:
                question.answer_set.create(type=choice['type'], text=choice['text'])
            self.object = question
            return self.render_to_response(self.get_context_data(), status=200)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


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
        question = self.object
        if question:
            data = json.loads(request.body)
            choices = data.get('choices', None)
            errors = {
                'errors': []
            }

            if choices is None:
                errors['errors'].append({'message': 'key "choices" not in request body'})
            elif not isinstance(choices, list):
                errors['errors'].append({'message': 'key "choices" must be list type'})
            elif len(choices) == 0:
                errors['errors'].append({'message': 'choices is empty list'})

            if errors['errors']:
                errors['status'] = 400
                return self.render_to_response(errors)

            for choice in choices:
                try:
                    answer = question.answer_set.get(id=choice['id'])
                    answer.type = choice['type']
                    answer.text = choice['text']
                    answer.save()
                except KeyError:
                    Answer.objects.create(question=question, text=choice['text'], type=choice['type'])
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        try:
            obj = super(PollUpdateView, self).get_object()
        except Http404:
            obj = None
        return obj

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
