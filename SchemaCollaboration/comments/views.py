from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from comments.forms import CommentForm
from core.models import Person


class AbstractAddComment(TemplateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._action_url = kwargs.pop('action_url')

    def get(self, request, *args, **kwargs):
        assert False

    def post(self, request, *args, **kwargs):
        datapackage_id = self.kwargs['datapackage_id']
        person = Person.objects.get(user=self.request.user)
        comment_form = CommentForm(request.POST, person=person, datapackage_id=datapackage_id, action_url=self._action_url)

        if comment_form.is_valid():
            comment_form.save()

            return redirect(reverse('management:datapackage-detail', kwargs={'pk': datapackage_id}))
        else:
            # TODO handle this
            assert False
