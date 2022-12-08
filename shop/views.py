import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from shop.models import Category, Candy
from shop.forms import CartAddForm, OrderForm
from django.conf import settings
from shop.services.category_service import CategoryService
from shop.services.order_service import OrderService
from shop.services.cart_item_service import CartItemServices


def categories_list(request):
    categories = CategoryService.all_categories()
    order_id = request.session.get('order_id')
    order = OrderService.get_or_create_order(request.user, order_id)
    if not request.user.is_authenticated:
        request.session['order_id'] = order.id
    candy_items = CartItemServices.get_candy_items_by_order(order)
    context = {
        'categories': categories,
        'candy_items_count': candy_items.count(),
    }
    return render(request, 'home.html', context)


def candies_list(request, category_slug):
    order_id = request.session.get('order_id')
    order = OrderService.get_or_create_order(request.user, order_id)
    if not request.user.is_authenticated:
        request.session['order_id'] = order.id
    candy_items = CartItemServices.get_candy_items_by_order(order)
    category = get_object_or_404(Category, slug=category_slug)
    candies = category.candies.all()
    context = {
        'category': category,
        'candies': candies,
        'candy_items_count': candy_items.count(),
    }
    return render(request, 'category_detail.html', context)


def add_to_cart(request, candy_id):
    candy = get_object_or_404(Candy, pk=candy_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        order_id = request.session.get('order_id')
        order = OrderService.get_or_create_order(user=request.user,
                                                 order_id=order_id)
        if not request.user.is_authenticated:
            request.session['order_id'] = order.id
        CartItemServices.add_cart_item(candy=candy, order=order, amount=amount)
        messages.info(request, "item added to cart")
    return redirect('candies_list', category_slug=candy.category.slug)


def get_cart(request):
    if request.method == 'GET':
        order_form = OrderForm(
            {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone_number': request.user.profile.number,
            } if request.user.is_authenticated else None
        )
    else:
        now = datetime.datetime.now()
        if now.hour < settings.START_WORK_TIME or now.hour > settings.END_WORK_TIME:
            messages.error(request, messages.INFO,
                           'Delivery is not carried out at this time')
            return redirect('cart')
        order_form = OrderForm(request.POST)
        order_id = request.session.get('order_id')
        if order_form.is_valid():
            OrderService.submit_order(request.user, order_form, order_id)
            messages.add_message(request,
                                 messages.INFO, 'Thank you for your order')
            return redirect('home')
    order_id = request.session.get('order_id')
    order = OrderService.get_or_create_order(request.user, order_id)
    if not request.user.is_authenticated:
        request.session['order_id'] = order.id
    candy_items = CartItemServices.get_candy_items_by_order(order)
    candy_items = CartItemServices.calculate_total_for_each_candy_item(candy_items)
    total_price = CartItemServices.calculate_total_price(candy_items)
    context = {
        'candy_items': candy_items,
        'total_price': total_price,
        'order_form': order_form,
        'candy_items_count': candy_items.count(),
    }
    return render(request, 'cart.html', context)
