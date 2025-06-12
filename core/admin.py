from django.contrib import admin
from .models import Category, SubCategory, Brand, Product
from django.db.models import Avg

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'subcategory', 'price', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'brand__name', 'subcategory__name')
    list_filter = ('brand', 'subcategory')
    ordering = ('-price',)

    def rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating.short_description = 'Average Rating'

