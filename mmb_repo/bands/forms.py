# __author__ = 'delhivery'

from __future__ import absolute_import, unicode_literals
from django import forms
from django.forms.formsets import BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field
from django.contrib.auth import get_user_model

from mmb_repo.mmb_data.models import Genre, Instrument
from .models import Band, BandMember, BandVacancy
from .app_settings import MEMBER_TYPE, CITIES


class BandVacancyForm(forms.ModelForm):
    instrument = forms.ModelChoiceField(queryset=Instrument.objects.none())
    type = forms.ChoiceField(choices=MEMBER_TYPE)

    class Meta:
        model = BandVacancy
        fields = ('instrument', 'type')

    def __init__(self, *args, **kwargs):
        super(BandVacancyForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.all()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'instrument',
            'type',

            ButtonHolder(
                Submit('submit', 'Create Vacancy', css_class='button white')
            )
        )


class BandMemberForm(forms.Form):
    member = forms.ModelChoiceField(queryset=((0,0),))
    instrument = forms.ModelChoiceField(queryset=Instrument.objects.none())
    type = forms.ChoiceField(choices=MEMBER_TYPE)

    def __init__(self, *args, **kwargs):
        super(BandMemberForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = get_user_model().objects.all()
        self.fields['instrument'].queryset = Instrument.objects.all()
        self.fields['member'].widget.attrs['class'] = 'controls textInput form-control chosen'
        self.fields['instrument'].widget.attrs['class'] = 'controls textInput form-control chosen'
        self.fields['type'].widget.attrs['class'] = 'controls textInput form-control chosen'


class BandForm(forms.ModelForm):
    genre = forms.MultipleChoiceField(label='Genre',
                                      widget=forms.SelectMultiple(attrs={'class': 'controls textInput form-control chosen'}))

    class Meta:
        model = Band
        fields = ('name', 'location', 'label', 'year', 'desc')

    def __init__(self, *args, **kwargs):
        super(BandForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(i.genre, i.genre) for i in Genre.objects.all()]
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control'})
        self.fields['label'].widget = forms.TextInput(attrs={'class': 'controls textInput form-control'})
        self.fields['desc'].widget = forms.Textarea(attrs={'class': 'controls textInput form-control', 'rows': 4})
        self.fields['location'].widget.attrs['class'] = 'controls textInput form-control'
        self.fields['year'].widget.attrs['class'] = 'controls textInput form-control'


class BaseBandFormset(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return


# class BandUploadSongForm(forms.ModelForm):
#
#     class Meta:
#         model = BandSong
#         fields = ("tags", "name", "upload",)
#
#     def __init__(self, *args, **kwargs):
#         super(BandUploadSongForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#            Field('upload', css_class="btn btn-success form-control "),
#              HTML("""
#              <br>
#             <p>
#             Name must be relevant to song, <strong>please set name accordingly.</strong></p>
#         """),
#            Field('name'),
#            Field('tags'),
#             ButtonHolder(
#                 Submit('submit', 'Submit', css_class='button white')
#             )
#         )
#
#     def clean_upload(self):
#         cleaned_data = super(BandUploadSongForm, self).clean()
#         file = cleaned_data.get('upload',False)
#         if file:
#             if file._size > 15*1024*1024:
#                 raise ValidationError("Audio file too large ( > 15mb )")
#             if not file.content_type in ["audio/mpeg","video/mp4","audio/mp3"]:
#                 raise ValidationError("Content-Type is not mpeg")
#             if not os.path.splitext(file.name)[-1] in [".mp3",".wav",".mp4"]:
#                 raise ValidationError("Doesn't have proper extension")
#              # Here we need to now to read the file and see if it's actually
#              # a valid audio file. I don't know what the best library is to
#              # to do this
#             # if not some_lib.is_audio(file.content):
#             #     raise ValidationError("Not a valid audio file")
#             return file
#         else:
#             raise ValidationError("Couldn't read uploaded file")

