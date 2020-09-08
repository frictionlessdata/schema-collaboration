from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.forms import ModelForm
from django.urls import reverse

from core.models import Datapackage
from .models import Comment


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        datapackage_id = kwargs.pop('datapackage_id')
        person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['text'].widget.attrs = {'rows': 3}

        self.fields['author'].initial = person
        self.fields['author'].disabled = True

        self.fields['datapackage'].initial = Datapackage.objects.get(id=datapackage_id)
        self.fields['datapackage'].disabled = True

        self.helper.layout = Layout(
            Div(
                Div('text', css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div('private', css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div('author', css_class='col-6'),
                Div('datapackage', css_class='col-6'),
                css_class='row',
                hidden=True
            ),
            FormActions(
                Submit('save', 'Add Comment'),
            )
        )

        self.helper.form_action = reverse('comments:add', kwargs={'datapackage_id': datapackage_id})

    class Meta:
        model = Comment
        fields = ['datapackage', 'author', 'text', 'private']
