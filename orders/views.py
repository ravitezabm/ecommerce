from django.shortcuts import render

def show_cart(request):
    return render(request,'cart.html')
