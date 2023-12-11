from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from django.contrib.auth.hashers import check_password


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
        if CustomUser.objects.filter(is_active=True).exists():
            return redirect('home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.get_by_email(email)
            if user and check_password(password, user.password):
                request.session['user_id'] = user.user_id
                CustomUser.objects.filter(user_id=user.user_id).update(is_active=True)
                return redirect('home')
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid email or password.'})
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    @staticmethod
    def get(request):
        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
            CustomUser.objects.filter(user_id=user_id).update(is_active=False)
            del request.session['user_id']
        return redirect('main')


class HomeView(View):
    template_name_participant = 'participant/participant.html'
    template_name_coach = 'coach/coach.html'

    def get(self, request):
        user_id = request.session.get('user_id')
        role = CustomUser.get_by_id(user_id).role
        context = {}

        if user_id:
            user = CustomUser.get_by_id(user_id)
            context['user'] = user

        if user_id and role == 'participant':
            return render(request, self.template_name_participant, context)
        else:
            return render(request, self.template_name_coach, context)


class MainView(View):
    template_name = 'main/main.html'

    def get(self, request):
        return render(request, self.template_name)
