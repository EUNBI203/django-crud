# from IPython import embed
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('articles:index')
    else:
        user_form = UserCreationForm()
    context = {
        'user_form': user_form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'Form': form
    }
    return render(request, 'accounts/login.html', context)