# __author__ = 'delhivery'

from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field
from django.contrib.auth import get_user_model

from mmb_repo.mmb_data.models import Genre, Instrument
from .models import Band, BandMember


class BandMemberForm(forms.ModelForm):
    instrument = forms.MultipleChoiceField(label='Instrument',
                                      choices=[(i.instrument, i.instrument) for i in Instrument.objects.all()],
                                      widget=forms.SelectMultiple(attrs={'class': 'form-control col-md-6 instrument'}))

    member = forms.ChoiceField(label="member",
                               choices=[(i.username, i.username) for i in get_user_model().objects.all()],
                               widget=forms.SelectMultiple(attrs={'class': 'controls textInput form-control col-md-3 member'}))

    class Meta:
        model = BandMember
        fields = ('type', )

    def __init__(self, *args, **kwargs):
        super(BandMemberForm, self).__init__(*args, **kwargs)
        # self.fields['member'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control col-md-3'})
        self.fields['type'].widget = forms.TextInput(attrs={'class': 'from-control col-md-1'})


class BandForm(forms.ModelForm):
    genre = forms.MultipleChoiceField(label='Genre',
                                      choices=[(i.genre, i.genre) for i in Genre.objects.all()],
                                      widget=forms.SelectMultiple(attrs={'class': 'controls textInput form-control genre'}))


    class Meta():
        model = Band
        fields = ('name', 'location', 'label', 'year', 'desc')


    def __init__(self, *args, **kwargs):
        super(BandForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control'})
        self.fields['location'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control'})
        self.fields['label'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control'})
        self.fields['year'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control'})
        self.fields['desc'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control'})


class BaseBandFormset(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return


