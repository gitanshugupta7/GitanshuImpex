from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('products/<slug:category_slug>/', views.category_products, name='category_detail'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('global-presence/', views.global_presence, name='global_presence')
    
    # Additional URL patterns can be added here
]
