from django.shortcuts import render
from django.db.models import Count, Q
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(total_products=Count('products'))

    # Filtering
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')

    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'search_query': search_query
    }
    return render(request, 'products/product_list.html', context)
