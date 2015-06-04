import json

from celery.bin.celery import inspect

from django.views.generic import FormView
from django.views.generic import View
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse

from celeryswamp.uploader.tasks import process_file
from .forms import UploadForm


class UploadView(FormView):
    template_name = 'uploader/base.html'
    form_class = UploadForm

    task_id = None

    def get_task_id(self):
        if self.task_id:
            return self.task_id
        self.task_id = self.request.GET.get('task_id', None)

        return self.task_id

    def get_success_url(self):
        return u'{0}?task_id={1}'.format(reverse('upload'), self.get_task_id())

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)

        context.update({
            'task_id': self.get_task_id()
        })

        return context

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        content = uploaded_file.read()
        uploaded_file.close()

        # Remove any previous results.
        async_result = process_file.delay(content)
        self.task_id = async_result.task_id

        return super(UploadView, self).form_valid(form)


class ProcessStatusView(View):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id', None)
        data = {
            'status': 'FAILURE',
            'current': 0,
            'total': 0,
        }

        async_result = process_file.AsyncResult(task_id)

        if async_result:
            data['status'] = async_result.state
            if async_result.state == 'PROGRESS':
                data.update(async_result.info)

        return HttpResponse(
            json.dumps(data),
            content_type='application/json'
        )
