# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import ValidationError

import validators
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field

from .models import User, Profile
from mmb_repo.mmb_data.models import Genre, Instrument, Songs


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
        choices=[(i.instrument,i.instrument) for i in Instrument.objects.all()],widget=forms.SelectMultiple(attrs={'class':'instrument'})   )

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
        model = Songs
        fields = ("tags", "name", "upload",)

    def __init__(self, *args, **kwargs):
        super(UploadSongForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'upload',
            'name',
            'tags',
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


