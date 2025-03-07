from django.shortcuts import render,redirect
from .models import Product
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages

def index(request):
    product_featured = Product.objects.order_by('priority')[:4]
    latest_featured = Product.objects.order_by('-id')[:8]
    context = {
        'featured_product':product_featured,
        'latest_featured':latest_featured
    }
    return render(request,'index.html',context)

def list_products(request):
    """
    returns products list
    """
    page =1
    if request.GET:
        page=request.GET.get('page',1)
    product_list =Product.objects.order_by('priority')
    product_paginator =Paginator(product_list,8)
    product_list = product_paginator.get_page(page)
    context = {'products':product_list}
    return render(request,'products.html',context)

def detail_products(request,pk):
    product = Product.objects.get(pk=pk)
    context = {'product':product}
    return render(request,'product_detailed.html',context)

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send an email to site admin
            send_mail(
                subject=f'New Contact Form Submission from {name}',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email=email,
                recipient_list=['abhiramanrs200@gmail.com'],  # Admin Email
            )

            # Send auto-reply email to user
            send_mail(
                subject="Thank you for contacting us!",
                message=f"Hi {name},\n\nThank you for reaching out! We have received your message and will get back to you soon.\n\nBest Regards,\nAbhiraman",
                from_email='abhiramanrs200@gmail.com',
                recipient_list=[email],  # Send to user's email
            )

            messages.success(request, "Your message has been sent successfully!")  # Success message
            return redirect('contact')  # Redirect back to the contact page

    else:
        form = ContactForm()
    return render(request,'contact.html',{'form': form})
