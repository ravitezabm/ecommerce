from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator

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
