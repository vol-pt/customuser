from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View
from django.contrib import messages
from django import forms

from .models import CustomUser


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField()
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean_remember_me(self):
        if not self.cleaned_data.get('remember_me', ''):
            self.request.session.set_expiry(0)


class CustomForm(UserCreationForm):
    error_css_class = 'ui error'

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(CustomLoginForm, self).__init__(*args, **kwargs)


def index(request):
    if request.user.is_authenticated:
        return redirect('/accounts/profile/')
    form = CustomForm()
    if request.method == 'POST':
        print(request.POST)
        form = CustomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'index.html', {'form': form})
    return render(request, 'index.html', {'form': form})


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    authentication_form = EmailAuthenticationForm


class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')
