from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthForm

class LoginRegisterView(View):
    def get(self, request):
        return render(request, 'accounts/login_register.html', {
            'register_form': CustomUserCreationForm(),
            'login_form': CustomAuthForm(),
            'active_form': 'login',  # თავიდან ლოგინი ჩანს
        })

    def post(self, request):
        if 'register' in request.POST:
            reg_form = CustomUserCreationForm(request.POST)
            login_form = CustomAuthForm()
            if reg_form.is_valid():
                user = reg_form.save()
                login(request, user)
                return redirect('core:index')
            else:
                return render(request, 'accounts/login_register.html', {
                    'register_form': reg_form,
                    'login_form': login_form,
                    'active_form': 'register',
                })

        elif 'login' in request.POST:
            login_form = CustomAuthForm(data=request.POST)
            reg_form = CustomUserCreationForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('core:index')
            else:
                return render(request, 'accounts/login_register.html', {
                    'login_form': login_form,
                    'register_form': reg_form,
                    'active_form': 'login',
                })
        else:
            return render(request, 'accounts/login_register.html', {
                'register_form': CustomUserCreationForm(),
                'login_form': CustomAuthForm(),
                'active_form': 'login',
            })

