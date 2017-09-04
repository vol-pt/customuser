from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean_remember_me(self):
        if not self.cleaned_data.get('remember_me', None):
            # Flush session at browser close
            self.request.session.set_expiry(0)


class CustomCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=True)
    gender = forms.ChoiceField(choices=(('m', 'Male'), ('f', 'Female'), ('o', 'Pre')), required=False)
    accept_tos = forms.BooleanField(required=False, label="Accept TOS")

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def clean_date_of_birth(self):
        print(self.cleaned_data)

