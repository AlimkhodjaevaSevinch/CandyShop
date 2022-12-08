from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Candy(models.Model):
    title = models.CharField(max_length=64, verbose_name='title')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='candies',
        verbose_name='category'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='orders'
    )
    first_name = models.CharField(max_length=150, verbose_name='first_name')
    last_name = models.CharField(max_length=150, verbose_name='last_name')
    email = models.EmailField(max_length=254, verbose_name='email')
    phone_number = models.CharField(max_length=16, verbose_name='phone_number')
    address = models.CharField(max_length=255, verbose_name='address')
    comment = models.CharField(max_length=255, verbose_name='comment')
    delivery_time = models.DateTimeField(
        verbose_name='delivery_time',
        null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ {self.id}"


class CandyItem(models.Model):
    candy = models.ForeignKey(
        Candy,
        on_delete=models.CASCADE,
        related_name='candy_items'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='candy_items'
    )
    amount = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.candy}"
