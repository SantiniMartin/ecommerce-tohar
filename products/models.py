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

    def calc_discount(self, percentage):
        return self.price * (1 - percentage / 100)

    def __str__(self):
        return self.name
