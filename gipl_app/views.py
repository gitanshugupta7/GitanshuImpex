from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .forms import InquiryForm
from .models import *

def home(request):
    categories = ProductCategory.objects.all()
    carousel_items = CarouselItem.objects.all()
    testimonials = Testimonial.objects.all()
    
    return render(request, 'gipl_app/home.html', {
        'categories': categories,
        'carousel_items': carousel_items,
        'testimonials': testimonials,
    })

def about(request):
    return render(request, 'gipl_app/about.html')

def products(request):
    categories = ProductCategory.objects.all()
    return render(request, 'gipl_app/products.html', {'categories': categories})

def category_products(request, category_slug):
    category = ProductCategory.objects.get(slug=category_slug)
    products = category.products.all()
    return render(request, 'gipl_app/category_products.html', {'category': category, 'products': products})

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    return render(request, 'gipl_app/product_detail.html', {'product': product})

def global_presence(request):
    return render(request, 'gipl_app/global_presence.html')

def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            # Send thank-you email to user
            subject = "Thank You for Contacting GIPL"
            message = (
                f"Dear {inquiry.name},\n\n"
                "Thank you for reaching out to Gitanshu Impex Pvt. Ltd. We have received your inquiry and will get back to you soon.\n\n"
                "Best regards,\n"
                "GIPL Team"
            )
            send_mail(
                subject,
                message,
                'gitanshuimpex@gmail.com',
                [inquiry.email],
                fail_silently=False
            )
            messages.success(request, "Your inquiry has been submitted successfully!")
            return redirect(request.path)
        else:
            messages.error(request, "Please correct the errors below.")
    
    # No need to pass the form here anymore (context processor handles it)
    return render(request, 'gipl_app/contact.html')

