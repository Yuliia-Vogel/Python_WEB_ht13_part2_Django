# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('quote_list') # куди перекидає при натисканні кнопки "зареєструватися"
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('quote_list') # куди перекидає при натисканні кнопки "розлогінитися"
    return render(request, 'users/logout.html') 


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "You logged in successfully!")
            return redirect('quote_list')
        else:
            messages.error(request, "Login error. Please try again.")
    else:
        messages.info(request, "Enter the system please. Registered users only can add new authors and quotes.")
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'