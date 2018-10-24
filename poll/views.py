import json
from django.http import JsonResponse, Http404
from django.views.generic.edit import BaseUpdateView
from .models import Question, Answer


class JSONResponseMixin:

    def render_to_json_response(self, context, **response_kwargs):
        status_code = context.get('status')
        if status_code:
            response_kwargs['status'] = status_code
        return JsonResponse(
            context,
            safe=False,
            **response_kwargs
        )

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_json_response(self.get_context_data())


class PollView(JSONResponseMixin, BaseUpdateView):
    model = Question

    def get(self, request, *args, **kwargs):
        return super(PollView, self).get(request, *args, **kwargs)

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
                return JsonResponse(errors)

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
            obj = super(PollView, self).get_object()
        except Http404:
            obj = None
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        question = self.object
        if self.object:
            context['question'] = {'id': question.id, 'text': question.text}
            context['status'] = 200
            context['choices'] = []
            for choise in question.answer_set.all():
                context['choices'].append({"id": choise.id, "type": choise.type, "text": choise.text})
        else:
            error = 'Object with id = %s, does not exist' % self.kwargs.get(self.pk_url_kwarg)
            context['error'] = error
            context['status'] = 404
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


