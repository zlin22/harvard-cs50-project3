from django.db import models

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    num_of_additions = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.size}): ${self.price}"

# class Order(models.Model):
#     is_complete = models.CharField(max_length=1)
