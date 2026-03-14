from django.contrib import admin
from .models import *
admin.site.register(Testimonial)
admin.site.register(Inquiry)
@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'cta_text', 'cta_link')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    # Added subdomain_prefix so you can see it in the main table view
    list_display = ('name', 'subdomain_prefix', 'slug') 
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}