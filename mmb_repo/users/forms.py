# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from .models import User, Profile


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just the name field.
        fields = ("name", )


class ProfileForm(forms.ModelForm):
    # about_me = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ("genre", "instrument", "college", "current_city", "phone", "website", "about_me", )
