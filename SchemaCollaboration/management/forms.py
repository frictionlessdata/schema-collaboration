from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms
from django.forms import RadioSelect

from core.models import Person, Datapackage


class PersonModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div('full_name', css_class='col-6'),
                css_class='row'
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = Person
        fields = ['full_name']


class DatapackageModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['status'].queryset = self.fields['status'].queryset.order_by('name')
        self.fields['collaborators'].queryset = self.fields['collaborators'].queryset.order_by('full_name')
        self.fields['collaborators'].help_text = 'Hold down “Control”, or “Command” on a Mac, to select more than one'
        self.fields['collaborators'].widget.attrs = {'size': 10}

        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div('status', css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div('collaborators', css_class='col-6'),
                css_class='row'
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = Datapackage
        fields = ['name', 'status', 'collaborators']
        widgets = {'status': RadioSelect}
