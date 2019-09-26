from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.contrib.auth.views import LogoutView


class SignUpView(BSModalCreateView):
    """
    A view that displays sign up form in modal
    """
    form_class = CustomUserCreationForm
    template_name = 'login_singup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('todo_app:index')
    extra_context = dict(title="Sing up")

class CustomLoginView(BSModalLoginView):
    """
    A view that displays login form in modal
    """
    authentication_form = CustomAuthenticationForm
    template_name = 'login_singup.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('todo_app:index'), title="Log in")

class CustomLogoutView(LogoutView):
    """
    NOT USED YET
    A view that provides logout message
    """
    def get_next_page(self):
        #next_page = super(LogoutView, self).get_next_page()
        messages.add_message(
            self.request, messages.SUCCESS,
            'You successfully log out!'
        )
        super().get_next_page()
        #return next_page