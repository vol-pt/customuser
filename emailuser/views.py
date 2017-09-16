from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import ListView

from .forms import EmailUserAuthenticationForm, EmailUserCreationForm
from .models import EmailUser


def register(request):
    # this view is for non-authenticated users only
    if request.user.is_authenticated:
        return redirect(reverse('profile_accounts'))

    # create empty form
    form = EmailUserCreationForm()
    if request.method == 'POST':
        # populate form with data
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            # if form is valid try to save and authenticate user
            form.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'User created!')
            return redirect('/accounts/profile/')
        # return form with error messages
        return render(request, 'emailuser/register.html', {'form': form})
    # GET
    return render(request, 'emailuser/register.html', {'form': form})


class EmailUserLogin(LoginView):
    redirect_authenticated_user = True
    template_name = 'emailuser/login.html'
    authentication_form = EmailUserAuthenticationForm


class ProfileView(View):
    def get(self, request):
        return render(request, 'emailuser/profile.html')


class CustomLogoutView(LogoutView):
    template_name = 'emailuser/register.html'
    next_page = '/'


class UserListView(ListView):
    model = EmailUser
    template_name = 'emailuser/users.html'
    paginate_by = 4
    ordering = '-date_joined'
