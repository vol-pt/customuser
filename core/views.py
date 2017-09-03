from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View
from django.contrib import messages
from django import forms

from .models import CustomUser


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': ''}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean_remember_me(self):
        if not self.cleaned_data.get('remember_me', ''):
            # Flush session at browser close
            self.request.session.set_expiry(0)


class CustomCreationForm(UserCreationForm):
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(choices=(('m', 'Male'), ('f', 'Female')), required=False)
    accept_tos = forms.BooleanField(required=True, help_text="Accept tos", label="Accept TOS")

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


def index(request):
    if request.user.is_authenticated:
        return redirect('/accounts/profile/')
    form = CustomCreationForm()
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created!')
            return redirect('/accounts/profile/')
        return render(request, 'index.html', {'form': form})
    return render(request, 'index.html', {'form': form})


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    authentication_form = EmailAuthenticationForm


class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')
