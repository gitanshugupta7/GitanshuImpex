from django.contrib import admin
from .models import Subdomain, ProductCategory, Product, Testimonial, Inquiry, CarouselItem

@admin.register(Subdomain)
class SubdomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix', 'meta_title')
    search_fields = ('name', 'prefix')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'slug') 
    list_filter = ('subdomain',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'cta_text', 'cta_link')

admin.site.register(Testimonial)
admin.site.register(Inquiry)