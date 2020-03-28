from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class MenuItemAddition(models.Model):
    desc = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.desc}"


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_num_of_additions = models.IntegerField(default=0)
    sort_id_asc = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_id_asc', '-size']

    def __str__(self):
        return f"{self.category}: {self.name} ({self.size}): ${self.price}"

class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="orders")
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_placed = models.CharField(max_length=1, default="N")

    def __str__(self):
        return f"{self.customer.username}'s order (${self.grand_total})"

class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name="orderItems")
    menu_item_addition = models.ManyToManyField(MenuItemAddition, blank=True, related_name="orderItems")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderItems", default=1, blank=True)

    def __str__(self):
        return f"{self.menu_item}"

