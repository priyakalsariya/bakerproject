from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse


# Create your views here.
def register_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password:
            messages.error(
                request,
                'Please enter username and password'
            )
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Username already exists'
            )
            return redirect('register')

        if password != confirm_password:
            messages.error(
                request,
                'Password and confirm password do not match'
            )
            return redirect('register')

        if not email or not email.endswith('@gmail.com'):
            messages.error(
                request,
                'Please enter a valid Gmail address'
            )
            return redirect('register')


        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )


    
        login(request, user)

        return redirect('index')


    return render(request, 'register.html')
            
def login_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user is None:
            messages.error(request,'Invalid username or password')
            return redirect('login')

        login(request,user)
        return redirect('index')
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request,"Your message has been sent successfully")
        return redirect('contact')
    return render(request,'contact.html')

def product(request):
    categories=Category.objects.all()

    search_query=request.GET.get('search','').strip()

    if search_query:
        products=Product.objects.filter(name__icontains=search_query)|Product.objects.filter(description__icontains=search_query)
    else:
        products=Product.objects.none()

    return render(request,'product.html',{'categories':categories,'search_query':search_query,'products':products})


def category_products(request,category_id):
    category=get_object_or_404(Category,id=category_id)

    products=Product.objects.filter(category=category)

    return render(request,'category_products.html',{'category':category,'products':products})

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product
        }
    )

def service(request):
    return render(request,'service.html')

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')

def error(request):
    return render(request,'404.html')

def read_more_about(request):
    return render(request,'read_more_about.html')

@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def edit_profile(request):
    user=request.user
    if request.method=="POST":
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email=request.POST.get('email')

        user.save()
        messages.success(request,'Profile Updated Successfully')

        return redirect('profile')
    return render(request,'edit_profile.html')

@login_required
def add_to_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)

    cart,created=Cart.objects.get_or_create(
        user=request.user
    )

    cart_item,created=CartItems.objects.get_or_create(
        cart=cart,
        products=product
    )

    if not created:
        cart_item.quentity+=1
        cart_item.save()

    return redirect('cart')

@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.all()

    total = sum(
        item.total_price
        for item in cart_items
    )

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def update_cart(request, item_id, change):

    change = int(change)

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItems,
        id=item_id,
        cart=cart
    )

    # Increase
    if change == 1:
        cart_item.quentity += 1

    # Decrease
    elif change == -1:
        cart_item.quentity -= 1

    # Remove item if quantity becomes 0
    if cart_item.quentity <= 0:

        cart_item.delete()

        cart_total = sum(
            item.total_price
            for item in cart.items.all()
        )

        return JsonResponse({
            'success': True,
            'deleted': True,
            'quantity': 0,
            'item_total': '0',
            'cart_total': str(cart_total)
        })

    cart_item.save()

    cart_total = sum(
        item.total_price
        for item in cart.items.all()
    )

    return JsonResponse({
        'success': True,
        'deleted': False,
        'quantity': cart_item.quentity,
        'item_total': str(cart_item.total_price),
        'cart_total': str(cart_total)
    })

@login_required
def remove_from_cart(request, item_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItems,
        id=item_id,
        cart=cart
    )

    cart_item.delete()

    # Recalculate cart total
    cart_total = sum(
        item.total_price
        for item in cart.items.all()
    )

    return JsonResponse({
        'success': True,
        'cart_total': str(cart_total)
    })

