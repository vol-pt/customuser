from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from dateutil import relativedelta

from .models import CustomUser


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean_remember_me(self):
        if not self.cleaned_data.get('remember_me', None):
            # Flush session at browser close
            self.request.session.set_expiry(0)
        return self.cleaned_data.get('remember_me')


class CustomCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    date_of_birth = forms.DateField(required=True)
    gender = forms.ChoiceField(choices=(('m', 'Male'), ('f', 'Female'), ('o', 'Pre')), required=False)
    accept_tos = forms.BooleanField(required=True, label="Accept TOS")

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'date_of_birth')

    def clean_date_of_birth(self):
        date = self.cleaned_data.get('date_of_birth')
        today = datetime.date(datetime.now())
        if date > today:
            raise ValidationError("You're born in the future congrats!", code='invalid')
        if date < today - relativedelta.relativedelta(years=130):
            raise ValidationError("You're 130 years+ old good for you!", code='invalid')
        return date

    def clean_accept_tos(self):
        if not self.cleaned_data.get('accept_tos', None):
            raise ValidationError('TOS must be accepted', code='invalid')
        return self.cleaned_data['accept_tos']

    def save(self, commit=False):
        user = super(CustomCreationForm, self).save(commit)
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user
