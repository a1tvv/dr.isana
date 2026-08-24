from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.all()
    context = {
        'active_page': 'home',
        'bestsellers': products[:4],
        'new_products': products[:2],
    }
    return render(request, 'store/home.html', context)


def catalog(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    context = {
        'active_page': 'catalog',
        'products': products,
    }
    return render(request, 'store/catalog.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'active_page': 'catalog',
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)


def about(request):
    return render(request, 'store/about.html', {'active_page': 'about'})


def reviews(request):
    return render(request, 'store/reviews.html', {'active_page': 'reviews'})