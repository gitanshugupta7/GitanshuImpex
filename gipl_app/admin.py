from django.contrib import admin
from .models import *

admin.site.register(Testimonial)
admin.site.register(Inquiry)

# 1. New: Register the Subdomain Group to manage high-level prefixes
@admin.register(Subdomain)
class SubdomainGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix', 'meta_title')
    search_fields = ('name', 'prefix')

@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'cta_text', 'cta_link')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    # 2. Change: Display the 'subdomain' foreign key instead of a text prefix
    list_display = ('name', 'subdomain', 'slug') 
    list_filter = ('subdomain',) # Filter by subdomain to stay organized
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}