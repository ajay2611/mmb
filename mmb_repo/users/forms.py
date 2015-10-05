# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import ValidationError

import validators
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML, MultiField, Div, Field

from .models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        # Set this form to use the User model
        model = User

        # Constrain the UserForm to just the name field.
        fields = ("username", )


class ProfileDataForm(UserForm):
    # about_me = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ("genre", "instrument", "college", "current_city", "phone", "website", "about_me",)

    def __init__(self, *args, **kwargs):
        super(ProfileDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.label_class = 'col-lg-2'
        # self.helper.filed_class = 'col-lg-5'
        # self.helper.form_class =  'form-horizontal'
        self.helper.layout = Layout(
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
        phone = cleaned_data['phone']
        website = cleaned_data['website']
        if phone:
            try:
                int(phone)
            except (ValueError, TypeError):
                raise forms.ValidationError('Please enter a valid phone number')

        if website and not validators.url(website):
            self._errors['website'] = self.error_class(
                ["Please enter a valid website. For example 'http://makemyband.in'"])
        return cleaned_data
