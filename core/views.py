from django.shortcuts import render
from products.models import Category, Product

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.all()[:4]
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_products': featured_products
    })

def about(request):
    return render(request, 'core/about.html')

