from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import EmailAuthenticationForm, CustomCreationForm


def index(request):
    if request.user.is_authenticated:
        return redirect('/accounts/profile/')
    form = CustomCreationForm()
    if request.method == 'POST':

        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(email=user.email, password=form.cleaned_data['password1'])
            login(request, user)
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
