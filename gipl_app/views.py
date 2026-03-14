from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from .forms import InquiryForm
from .models import *

def home(request):
    # If on a subdomain (e.g., stationary.gitanshuimpex.com), ONLY fetch the stationary category
    if hasattr(request, 'subdomain') and request.subdomain:
        categories = ProductCategory.objects.filter(subdomain_prefix=request.subdomain)
    # If on the main domain (gitanshuimpex.com), fetch ALL categories
    else:
        categories = ProductCategory.objects.all()
        
    carousel_items = CarouselItem.objects.all()
    testimonials = Testimonial.objects.all()
    
    # Loads the exact same template regardless of domain
    return render(request, 'gipl_app/home.html', {
        'categories': categories,
        'carousel_items': carousel_items,
        'testimonials': testimonials,
    })

def about(request):
    return render(request, 'gipl_app/about.html')

def products(request):
    # Same logic as home: filter the products page based on where the user is
    if hasattr(request, 'subdomain') and request.subdomain:
        categories = ProductCategory.objects.filter(subdomain_prefix=request.subdomain)
    else:
        categories = ProductCategory.objects.all()
        
    return render(request, 'gipl_app/products.html', {'categories': categories})

def category_products(request, category_slug):
    category = get_object_or_404(ProductCategory, slug=category_slug)
    
    # Security/UX check: Don't allow loading the "hardware" category on the "stationary" subdomain
    if hasattr(request, 'subdomain') and request.subdomain:
        if category.subdomain_prefix != request.subdomain:
            return redirect('home')
            
    products = category.products.all()
    return render(request, 'gipl_app/category_products.html', {'category': category, 'products': products})

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    
    # Security/UX check: Don't allow loading a "hardware" product on the "stationary" subdomain
    if hasattr(request, 'subdomain') and request.subdomain:
        if product.category.subdomain_prefix != request.subdomain:
            return redirect('home')

    return render(request, 'gipl_app/product_detail.html', {'product': product})

def global_presence(request):
    return render(request, 'gipl_app/global_presence.html')

def contact(request):
    # (Your existing contact logic remains exactly the same)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            subject = "Thank You for Contacting GIPL"
            message = (
                f"Dear {inquiry.name},\n\n"
                "Thank you for reaching out to Gitanshu Impex Pvt. Ltd. We have received your inquiry and will get back to you soon.\n\n"
                "Best regards,\n"
                "GIPL Team"
            )
            send_mail(subject, message, 'gitanshuimpex@gmail.com', [inquiry.email], fail_silently=False)
            messages.success(request, "Your inquiry has been submitted successfully!")
            return redirect(request.path)
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'gipl_app/contact.html')

def global_inquiry(request):
    # (Your existing global_inquiry logic remains exactly the same)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            context = {'name': inquiry.name, 'year': datetime.now().year}
            html_content = render_to_string('gipl_app/email.html', context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject="Thank You for Contacting GIPL",
                body=text_content,
                from_email='gitanshuimpex@gmail.com',
                to=[inquiry.email],
                cc=['guptajiten@gmail.com']
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "Your inquiry has been submitted successfully!")
            return redirect(request.path)
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'gipl_app/contact.html')