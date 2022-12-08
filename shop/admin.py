from django.contrib import admin
from shop.models import Candy, Category, Order, CandyItem

admin.site.register(Candy)
admin.site.register(Category)
admin.site.register(CandyItem)
admin.site.register(Order)
