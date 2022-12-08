from shop.models import Order


class OrderService:
    @staticmethod
    def get_or_create_order_by_user(user):
        order, created = Order.objects.get_or_create(user=user, is_completed=False)
        return order

    @staticmethod
    def submit_order(user, order_form, order_id):
        order = OrderService.get_or_create_order(user=user, order_id=order_id)
        order.first_name = order_form.cleaned_data['first_name']
        order.last_name = order_form.cleaned_data['last_name']
        order.email = order_form.cleaned_data['email']
        order.phone_number = order_form.cleaned_data['phone_number']
        order.address = order_form.cleaned_data['address']
        order.delivery_time = order_form.cleaned_data['delivery_time']
        order.comment = order_form.cleaned_data['comment']
        order.is_completed = True
        order.save()

    @staticmethod
    def get_or_create_anonymous_order(order_id):
        if order_id:
            order = Order.objects.get(id=order_id)
        else:
            order = Order.objects.create()
        return order

    @staticmethod
    def get_or_create_order(user, order_id):
        if user.is_authenticated:
            order = OrderService.get_or_create_order_by_user(user=user)
        else:
            order = OrderService.get_or_create_anonymous_order(order_id)
        return order
