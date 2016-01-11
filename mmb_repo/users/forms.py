# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from django import forms
from django.core.exceptions import ValidationError

import validators
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field

from .models import User, Profile
from mmb_repo.mmb_data.models import Genre, Instrument, Song


class UserForm(forms.ModelForm):
    class Meta:
        # Set this form to use the User model
        model = User

        # Constrain the UserForm to just the name field.
        fields = ("username", )


class ProfileDataForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label="Username", error_messages={
                                'invalid': "This value must contain only letters, numbers and underscores."})

    genre = forms.MultipleChoiceField(label='Genre',
        choices=[(i.genre,i.genre) for i in Genre.objects.all()],widget=forms.SelectMultiple(attrs={'class':'genre'}))

    instrument = forms.MultipleChoiceField(label='Instrument',
        choices=[(i.instrument,i.instrument) for i in Instrument.objects.all()],widget=forms.SelectMultiple(attrs={'class':'instrument'}))

    class Meta:
        model = Profile
        fields = ("college", "current_city", "phone", "website", "about_me",)

    def __init__(self, *args, **kwargs):
        super(ProfileDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.label_class = 'col-lg-2'
        # self.helper.filed_class = 'col-lg-5'
        # self.helper.form_class =  'form-horizontal'
        self.helper.layout = Layout(
            'username',
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

        if website and not validators.url(website):
            self._errors['website'] = self.error_class(
                ["Please enter a valid website. For example 'http://makemyband.in'"])
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