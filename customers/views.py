from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def sign_out(request):
    logout(request)
    return redirect('index')

def show_account(request):
    if request.POST and 'register' in request.POST:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address =request.POST.get('address')
            phone = request.POST.get('phone')
            # creates user account
            user = User.objects.create_user(username=username,
                                       password=password,
                                       email=email)
            # create customer object
            customer=Customer.objects.create(user=user,
                                             name=username,
                                    phone=phone,
                                    address=address)
            message = "User Registered Successfully"
            messages.success(request,message)

        except Exception as e:
            error_message = "Duplicate Username or Invalid Credentials"
            messages.error(request,error_message)

    if request.POST and 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            message = "Invalid Credentials"
            messages.error(request,message)

    return render(request,'account.html')
