from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from comments.forms import CommentForm
from core.models import Person, Datapackage


class AbstractAddCommentView(TemplateView):
    def __init__(self, success_url, failure_url, *args, **kwargs):
        self._success_url = success_url
        self._failure_url = failure_url

        super().__init__(*args, **kwargs)
        print('test')

    def get(self, request, *args, **kwargs):
        assert False

    def post(self, request, *args, **kwargs):
        if 'datapackage_id' in kwargs:
            datapackage = Datapackage.objects.get(id=kwargs['datapackage_id'])
        elif 'datapackage_uuid' in kwargs:
            datapackage = Datapackage.objects.get(uuid=kwargs['datapackage_uuid'])
        else:
            assert False

        if self.request.user:
            person = Person.objects.get(user=self.request.user)
        else:
            person = None

        comment_form = CommentForm(request.POST, datapackage_id=datapackage.id, person=person)

        if comment_form.is_valid():
            comment_form.save()

            # return redirect(reverse('management:datapackage-detail', kwargs={'pk': datapackage_id}))
            return redirect(self._success_url)
        else:
            # TODO handle this
            assert False
