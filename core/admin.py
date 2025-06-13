from django.contrib import admin
from .models import Category, SubCategory, Brand, Product
from django.db.models import Avg

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'subcategory', 'price','quantity', 'slug')
    list_display_links = ('name',)
    list_editable = ('price','quantity',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'brand__name', 'subcategory__name')
    list_filter = ('brand', 'subcategory')
    ordering = ('-price',)
    readonly_fields = ('rating',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'price', 'quantity', 'brand', 'subcategory', 'image')
        }),
        ('Additional Information', {
            'fields': ('rating',),
            'classes': ('collapse',)
        }),
    )

    def rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating.short_description = 'Average Rating'

