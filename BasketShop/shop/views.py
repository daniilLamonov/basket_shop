from unicodedata import category

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from .models import Product, Category, Brand


# Create your views here.
def product_list(request, category_slug=None, brand_slug=None):
    products = Product.objects.filter(available=True)
    if category_slug and brand_slug:
        category = get_object_or_404(Category, slug=category_slug)
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(category=category, brand=brand)
        return render(request,
                      'shop/product_list.html',
                      {'products': products})
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=brand)
    products = pagination(products, request, 4)
    return render(request,
                  'shop/product_list.html',
                  {'products': products})

def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

def pagination(items, request, items_per_page=12):
    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page', 1)
    try:
        items = paginator.page(page_number)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items