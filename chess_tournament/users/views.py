from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from django.contrib.auth.hashers import check_password


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if CustomUser.objects.filter(is_active=True).exists():
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.get_by_email(email)
            print(user)
            if user and check_password(password, user.password):
                request.session['user_id'] = user.user_id
                CustomUser.objects.filter(user_id=user.user_id).update(is_active=True)
                return redirect('home')
            else:
                return render(request, 'login/login.html', {'form': form, 'error': 'Invalid email or password.'})
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})


def logout_view(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        CustomUser.objects.filter(user_id=user_id).update(is_active=False)
        del request.session['user_id']
    return redirect('main')


def home(request):
    user_id = request.session.get('user_id')
    role = CustomUser.get_by_id(user_id).role
    context = {}

    if user_id:
        user = CustomUser.get_by_id(user_id)
        context['user'] = user

    if role == 'participant':
        return render(request, 'participant/participant.html', context)

    else:
        return render(request, 'coach/coach.html', context)


def main(request):
    return render(request, 'main/main.html')

