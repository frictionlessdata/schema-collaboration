from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from comments.forms import CommentForm
from core.models import Person, Datapackage


class AbstractAddCommentView(TemplateView):
    def __init__(self, user, success_view_name, failure_url, *args, **kwargs):
        self._user = user
        self._success_view_name = success_view_name
        self._failure_url = failure_url

        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        assert False

    def post(self, request, *args, **kwargs):
        datapackage = Datapackage.objects.get(uuid=kwargs['uuid'])

        if self._user:
            person = Person.objects.get(user=self._user)
        else:
            person = None

        comment_form = CommentForm(request.POST, datapackage_id=datapackage.id, person=person)

        if comment_form.is_valid():
            comment_form.save()
            return redirect(reverse(self._success_view_name, kwargs={'uuid': datapackage.uuid}))

        else:
            # TODO handle this
            assert False
