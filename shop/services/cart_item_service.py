from shop.models import Order, CandyItem
from django.db.models import F, Sum


class CartItemServices:

    @staticmethod
    def add_cart_item(order, candy, amount: int):
        cart_item, created = CandyItem.objects.get_or_create(order=order, candy=candy)
        if created:
            cart_item.amount = amount
        else:
            cart_item.amount += amount
        cart_item.save()
        return cart_item

    @staticmethod
    def get_candy_items_by_order(order: Order):
        return order.candy_items.all()

    @staticmethod
    def calculate_total_for_each_candy_item(candy_items):
        return candy_items.annotate(total=F('candy__price') * F('amount'))

    @staticmethod
    def calculate_total_price(candy_items) -> float:
        return candy_items.aggregate(total_price=Sum('total'))['total_price']
