from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'login/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.get_by_email(email)

            if user and check_password(password, user.password) and (user.role == 'participant' or
                                                                     user.role == 'coach'):
                login(request, user)
                return redirect('home')
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid email or password.'})
        return render(request, self.template_name, {'form': form, 'error': 'Invalid email or password.'})


class LogoutView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('main')


class HomeView(View):
    template_name_participant = 'participant/participant.html'
    template_name_coach = 'coach/coach.html'
    template_name = 'user/user.html'

    def get(self, request):
        user = request.user
        context = {'user': user, 'permission_create_tournament': user.has_perm('tournaments.create_tournament'),
                   'permission_add_location': user.has_perm('locations.add_location')}

        return render(request, self.template_name, context)



class MainView(View):
    template_name = 'main/main.html'

    def get(self, request):
        return render(request, self.template_name)
