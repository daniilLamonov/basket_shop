from .models import Category, Brand


def categories_processor(request):
    return {'categories': Category.objects.all()}
def brands_processor(request):
    return {'brands': Brand.objects.all()}