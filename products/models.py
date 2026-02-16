from decimal import Decimal
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    class CategoryEnum(models.TextChoices): # Kept for reference but using FK as requested
        pass

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    # Using ForeignKey to Category as per request "agregues la categoría" implying a model
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(default=0)

    @property
    def final_price(self):
        if self.discount_percentage > 0:
            return self.price * (1 - Decimal(self.discount_percentage) / 100)
        return self.price


    def __str__(self):
        return self.name
