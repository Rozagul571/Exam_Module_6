import re
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from apps.models import User

class RegistrModelForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'password', 'username')


    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('Bu email allaqachon ro‘yxatdan o‘tgan.')
        return email

class VerifyForm(forms.Form):
    code = forms.IntegerField(label="Verification Code")
        # def clean_email(self):