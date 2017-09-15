from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import ListView

from .forms import EmailUserAuthenticationForm, EmailUserCreationForm
from .models import EmailUser


def index(request):
    if request.user.is_authenticated:
        return redirect('/accounts/profile/')
    form = EmailUserCreationForm()
    if request.method == 'POST':

        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'User created!')
            return redirect('/accounts/profile/')
        return render(request, 'emailuser/index.html', {'form': form})

    return render(request, 'emailuser/index.html', {'form': form})


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'emailuser/login.html'
    authentication_form = EmailUserAuthenticationForm


class ProfileView(View):
    def get(self, request):
        return render(request, 'emailuser/profile.html')


class CustomLogoutView(LogoutView):
    template_name = 'emailuser/index.html'
    next_page = '/'


class UserListView(ListView):
    model = EmailUser
    template_name = 'emailuser/users.html'
    paginate_by = 4
    ordering = '-date_joined'
