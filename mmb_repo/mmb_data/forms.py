# from __future__ import absolute_import, unicode_literals
#
# from django import forms
# from django.core.exceptions import ValidationError
#
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field
# from .models import Instrument
#
#
# class SearchForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         super(SearchForm, self).__init__(*args, **kwargs)
#         self.fields['q'] = forms.ChoiceField(choices=[(o.id, str(o)) for o in Instrument.objects.all()])
