from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from .models import Category, Product, SubCategory, Brand, Review
from django.db.models import Q, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm

class CategoryListView(ListView):
    model = Category
    template_name = 'core/index.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.prefetch_related('subcategories').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_list = Product.objects.select_related('subcategory').order_by('-created_at')
        paginator = Paginator(product_list, 4)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        for product in page_obj:
            product.avg_rating = round(product.average_rating, 2)

        context['products'] = page_obj
        context['subcategories'] = SubCategory.objects.all()
        context['brands'] = Brand.objects.all()
        context['page_obj'] = page_obj
        context['popular_products'] = Product.objects.order_by('-views')[:10]

        return context

class SubCategoryProductListView(ListView):
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(
            subcategory__slug=self.kwargs['slug']
        ).select_related('subcategory').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subcategory = SubCategory.objects.get(slug=self.kwargs['slug'])
        for product in context['products']:
            product.avg_rating = round(product.average_rating, 2)

        context['subcategory'] = subcategory
        return context

class ProductSearchView(ListView):
    model = Product
    template_name = 'core/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            ).select_related('subcategory').order_by('-created_at')
        return Product.objects.none()

class ProductFilterView(ListView):
    model = Product
    template_name = 'core/filtered_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        subcategory = self.request.GET.get('subcategory')
        brand = self.request.GET.get('brand')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if subcategory:
            queryset = queryset.filter(subcategory__slug=subcategory)
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        context['brands'] = Brand.objects.all()
        return context
    
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context['reviews'] = product.reviews.all()
        context['review_form'] = ReviewForm()

        average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        context['average_rating'] = round(average_rating, 2)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object

        if 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review, created = Review.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={
                        'rating': review_form.cleaned_data['rating'],
                        'comment': review_form.cleaned_data['comment'],
                    }
                )
                return redirect(product.get_absolute_url())

        context = self.get_context_data()
        context['review_form'] = review_form
        return self.render_to_response(context)