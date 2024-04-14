from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render

from goods.models import Products
from goods.utils import q_search


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    
    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = [good for good in goods if good.discount > 0]

    if order_by and order_by != "default":
        if order_by.startswith('-'):
            attribute_name = order_by[1:]  # Remove the '-' prefix
            reverse_sort = True
        else:
            attribute_name = order_by
            reverse_sort = False
        goods = sorted(goods, key=lambda x: getattr(x, attribute_name), reverse=reverse_sort)
        # if on_sale:
    #     goods = goods.filter(discount__gt=0)

    # if order_by and order_by != "default":
    #     goods = goods.order_by(order_by)

    paginator = Paginator(goods, 6)
    current_page = paginator.page(int(page))

    context = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {"product": product}

    return render(request, "goods/product.html", context=context)