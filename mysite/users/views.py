from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django import forms
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.success(request,'Invalid details. Try Again!')
                return redirect('login')
            
    else:
        login_form = LoginForm()
    return render(request,'users/login.html',{'login_form':login_form})


def user_logout(request):
    logout(request)
    messages.success(request, "You're logged-out.. Please login to continue!")
    return redirect('login')


def user_register(request):

    if request.method=="POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            print("Validation success")
            # login upon registration
            login(request, new_user)
            messages.success(request,'Hey! Welcome Onboard!')
            return redirect('index')
        else:
            print(user_form.errors)
        
    else:
        user_form = RegisterForm()
    return render(request,'users/register.html',{'user_form':user_form})
