from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order,OrderedItem
from products.models import Product
from django.contrib import messages


@login_required(login_url='account')
def show_cart(request):
    user = request.user
    customer= user.customer_profile
    cart_obj,created=Order.objects.get_or_create(
        owner = customer,
        order_status = Order.CART_STAGE
    )
    context = {'cart':cart_obj}
    return render(request,'cart.html',context)

@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user = request.user
        customer = user.customer_profile
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        cart_obj,created  =Order.objects.get_or_create(
            owner = customer,
            order_status = Order.CART_STAGE
        )
        product = Product.objects.get(pk=product_id)
        ordered_item,created = OrderedItem.objects.get_or_create(
            product = product,
            owner = cart_obj
        )
        if created:
            ordered_item.quantity = quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity + quantity
            ordered_item.save()
    return redirect('cart')
@login_required(login_url='account')
def remove_item_from_cart(request,pk):
    item = OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')

def view_orders(request):
    user = request.user
    customer= user.customer_profile

    return render(request,'cart.html',context)

@login_required(login_url='account')
def show_orders(request):
    user = request.user
    customer= user.customer_profile
    all_orders =Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context = {'orders':all_orders}
    return render(request,'orders.html',context)

@login_required(login_url='account')
def checkout_cart(request):
    try:
        if request.POST:
            user = request.user
            customer = user.customer_profile
            total = float(request.POST.get('total'))
            order_obj  =Order.objects.get(
                owner = customer,
                order_status = Order.CART_STAGE
            )
            if order_obj:
                 order_obj.order_status = Order.ORDER_CONFIRMED
                 order_obj.total_price = total
                 order_obj.save()
                 status_message = "Your Order is Processed.Your item will be delivered in two weeks"
                 messages.success(request,status_message)
            else:
                status_message = "Unable to process, No items in cart!"
                messages.success(request, status_message)
    except Exception as e:
        status_message = "Unable to process, No items in cart!"
        messages.success(request, status_message)
    return redirect('cart')





