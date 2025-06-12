from django.urls import path
from .views import CategoryListView, ProductSearchView, ProductFilterView, ProductDetailView, SubCategoryProductListView

app_name = 'core'

urlpatterns = [
    path('', CategoryListView.as_view(), name='index'),
    path('search/', ProductSearchView.as_view(), name='search_results'),
    path('filter/', ProductFilterView.as_view(), name='product_filter'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', SubCategoryProductListView.as_view(), name='product_list'),
]