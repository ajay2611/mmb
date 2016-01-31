# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import validators

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field

from .models import User, Profile
from mmb_repo.mmb_data.models import Genre, Instrument, Song
from .app_settings import USER_TYPE



class UserForm(forms.ModelForm):
    class Meta:
        # Set this form to use the User model
        model = User
        # Constrain the UserForm to just the name field.
        fields = ("username", )


class ProfileDataForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label="Username",
                                error_messages={
                                    'invalid': "This value must contain only letters, numbers and underscores."})

    type = forms.CharField(label='Type',
                           widget=forms.RadioSelect(attrs={'type': 'radio'}))

    genre = forms.MultipleChoiceField(label='Genre',
                                      widget=forms.SelectMultiple(attrs={'class': 'chosen'}),
                                      required=False)

    instrument = forms.MultipleChoiceField(label='Instrument',
                                           widget=forms.SelectMultiple(attrs={'class': 'chosen'}),
                                           required=False)

    class Meta:
        model = Profile
        fields = ("college", "current_city", "phone", "website", "about_me",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileDataForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(i.genre, i.genre) for i in Genre.objects.all()]
        self.fields['instrument'].choices = [(i.instrument, i.instrument) for i in Instrument.objects.all()]
        self.fields['about_me'].widget = forms.Textarea(attrs={'rows': 4})
        self.fields['type'].choices = USER_TYPE
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'type',
            'genre',
            'instrument',
            'college',
            'current_city',
            'phone',
            'website',
            'about_me',

            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    def clean(self):
        cleaned_data = super(ProfileDataForm, self).clean()
        website = cleaned_data['website']
        username = cleaned_data['username']
        type = cleaned_data['type']
        instrument = cleaned_data['instrument']

        if website and not validators.url(website):
            self._errors['website'] = self.error_class(
                ["Please enter a valid website. For example 'http://makemyband.in'"])

        if type == u'Musician':
            if not instrument:
                self._errors['instrument'] = self.error_class(
                ["This field is required"])

        try:
            user = get_user_model().objects.get(username=username)
            if user and (username != self.user.username):
                self._errors['username'] = self.error_class(
                ["Username already exists"])
        except:
            pass

        return cleaned_data


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label="Password", required=False,
                            widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                            widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'password1',
            'password2',
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


class UploadSongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ("tags", "name", "upload",)

    def __init__(self, *args, **kwargs):
        super(UploadSongForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
           Field('upload', css_class="btn btn-success form-control "),
             HTML("""
                 <br>
                <p>
                Name must be relevant to song, <strong>please set name accordingly.</strong></p>
        """),
           Field('name'),
           Field('tags'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    def clean_upload(self):
        cleaned_data = super(UploadSongForm, self).clean()
        file = cleaned_data.get('upload',False)
        if file:
            if file._size > 15*1024*1024:
                raise ValidationError("Audio file too large ( > 15mb )")
            if not file.content_type in ["audio/mpeg","video/mp4","audio/mp3"]:
                raise ValidationError("Content-Type is not mpeg")
            if not os.path.splitext(file.name)[-1] in [".mp3",".wav",".mp4"]:
                raise ValidationError("Doesn't have proper extension")
             # Here we need to now to read the file and see if it's actually
             # a valid audio file. I don't know what the best library is to
             # to do this
            # if not some_lib.is_audio(file.content):
            #     raise ValidationError("Not a valid audio file")
            return file
        else:
            raise ValidationError("Couldn't read uploaded file")
