from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from . import forms
from django.urls import reverse_lazy
from borrow.models import Borrowing
from core.utils import send_email
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

class RegisterView(FormView):
    template_name = './accounts/auth.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        context=  super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context
    
class UserLoginView(LoginView):
    template_name = './accounts/auth.html'
    
    def get_context_data(self, **kwargs) :
        context=  super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    def get_success_url(self):
        return reverse_lazy('profile')
    
def UserLogoutView(request):
    logout(request)
    return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    template_name = './accounts/profile.html'
    def get(self, request):
        return render(request, self.template_name, {'account':request.user.account})

    
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = './accounts/profile_update.html'
    def get(self, request):
        form = forms.ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})



class DepositeView(View):
    template_name = './accounts/deposite.html'
    def get(self, request, *args, **kwargs):
        form = forms.DepositeForm()
        return render(request, self.template_name, {'form':forms.DepositeForm()})
    
    def post(self, request, *args, **kwargs):
        form = forms.DepositeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('deposite_amount')
            request.user.account.deposite(amount)
            # send email
            message = render_to_string('./accounts/deposite_email.html', {
                'user': request.user,
                'amount':amount,
            })
            send_mail = EmailMultiAlternatives("Successfully Deposited Money", '', to=[request.user.email])
            send_mail.attach_alternative(message, 'text/html')
            send_mail.send()
            # redirect to the profile page
            return redirect('profile')
        return render(request, self.template_name, {'form': form})