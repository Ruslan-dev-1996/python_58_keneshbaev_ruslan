from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from accounts.forms import SignUpForm


def login_view(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('webapp:index')


def register_view(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'register.html', context={'form': form})
    elif request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data.get('username'))
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('webapp:index')
        else:
            return render(request, 'register.html', context={'form': form})
