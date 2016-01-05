# __author__ = 'delhivery'

from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field

from mmb_repo.mmb_data.models import Genre, Instrument
from .models import Band, BandMember


class BandMemberForm(forms.ModelForm):
    class Meta:
        model = BandMember
        fields = ('member', 'instrument', 'type')


class BandForm(forms.ModelForm):
    genre = forms.MultipleChoiceField(label='Genre',
                                      choices=[(i.genre, i.genre) for i in Genre.objects.all()],
                                      widget=forms.SelectMultiple(attrs={'class': 'genre'}))

    class Meta():
        model = Band
        fields = ('name', 'member', 'location', 'label', 'year', 'desc')

    def __init__(self, *args, **kwargs):
        super(BandForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'genre',
            'member',
            'location',
            'label',
            'year',
            'desc',

            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )