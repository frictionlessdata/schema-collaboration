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
        action_url = kwargs.pop('action_url')
        person = kwargs.pop('person', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['text'].widget.attrs = {'rows': 3}

        self.fields['private'].help_text = 'Enable if this comment is going to be visible only by you'

        if person:
            self.fields['author'].initial = person
            self.fields['author'].disabled = True
        else:
            self.fields['author'].queryset = Datapackage.objects.get(id=datapackage_id).\
                collaborators.order_by('full_name')
            self.fields['author'].help_text = 'Please select who you are'

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
                css_class='row',
                hidden=person is not None
            ),
            Div(
                Div('datapackage', css_class='col-6'),
                css_class='row',
                hidden=True
            ),

            FormActions(
                Submit('save', 'Add Comment'),
            )
        )


    class Meta:
        model = Comment
        fields = ['datapackage', 'author', 'text', 'private']
