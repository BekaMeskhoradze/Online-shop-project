from core.models import Product
from django.utils.deprecation import MiddlewareMixin

class ProductViewCountMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.resolver_match and request.resolver_match.view_name == 'core:product_detail':
            slug = view_kwargs.get('slug')
            if slug:
                try:
                    product = Product.objects.get(slug=slug)
                    product.views += 1
                    product.save(update_fields=['views'])
                except Product.DoesNotExist:
                    pass
        return None
