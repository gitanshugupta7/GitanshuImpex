from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from .forms import InquiryForm
from .models import *

def home(request):
    # 1. Identify the subdomain (e.g., 'stationary')
    # If you are using middleware that sets request.subdomain, use that.
    # Otherwise, we extract it from the host.
    subdomain_val = getattr(request, 'subdomain', None)
    
    if not subdomain_val:
        host_parts = request.get_host().split('.')
        if len(host_parts) > 2:
            subdomain_val = host_parts[0]

    # 2. Filter categories based on the NEW Foreign Key relationship
    if subdomain_val and subdomain_val not in ['www', 'gitanshuimpex']:
        # We use 'subdomain__prefix' to filter through the relationship
        categories = ProductCategory.objects.filter(
            subdomain__prefix=subdomain_val,
            subdomain__is_active=True
        )
        # Fetch subdomain-specific branding for the Hero section
        sub_info = Subdomain.objects.filter(prefix=subdomain_val).first()
    else:
        # Main domain shows everything
        categories = ProductCategory.objects.all()
        sub_info = None
        
    carousel_items = CarouselItem.objects.all()
    testimonials = Testimonial.objects.all()
    
    return render(request, 'gipl_app/home.html', {
        'categories': categories,
        'sub_info': sub_info, # Added to context for dynamic headers
        'carousel_items': carousel_items,
        'testimonials': testimonials,
    })

def about(request):
    host = request.get_host().split('.')
    subdomain_val = host[0] if len(host) > 2 else None
    sub_info = Subdomain.objects.filter(prefix=subdomain_val).first() if subdomain_val else None
    
    return render(request, 'gipl_app/about.html', {'sub_info': sub_info})

def global_presence(request):
    host = request.get_host().split('.')
    subdomain_val = host[0] if len(host) > 2 else None
    sub_info = Subdomain.objects.filter(prefix=subdomain_val).first() if subdomain_val else None
    
    return render(request, 'gipl_app/global_presence.html', {'sub_info': sub_info})

def products(request):
    host = request.get_host().split('.')
    subdomain_val = host[0] if len(host) > 2 else None

    # Fix: Filter through the Subdomain relationship
    if subdomain_val and subdomain_val not in ['www', 'gitanshuimpex']:
        categories = ProductCategory.objects.filter(
            subdomain__prefix=subdomain_val, 
            subdomain__is_active=True
        )
    else:
        categories = ProductCategory.objects.all()
        
    return render(request, 'gipl_app/products.html', {'categories': categories})

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product

# Change 'slug' to 'category_slug' to match your urls.py
def category_products(request, category_slug):
    # Use category_slug here
    category = get_object_or_404(ProductCategory, slug=category_slug)

    host = request.get_host().split('.')
    current_subdomain = host[0] if len(host) > 2 else None

    if current_subdomain and current_subdomain not in ['www', 'gitanshuimpex']:
        if not category.subdomain or category.subdomain.prefix != current_subdomain:
            from django.http import Http404
            raise Http404("Product category not found on this subdomain.")

    products = Product.objects.filter(category=category)

    return render(request, 'gipl_app/category_products.html', {
        'category': category,
        'products': products,
    })

# IMPORTANT: Remove the duplicate global_presence function at the bottom 
# of your views.py so it doesn't override the one with sub_info logic.
def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    
    host = request.get_host().split('.')
    current_subdomain = host[0] if len(host) > 2 else None

    # Fix: Check the relationship instead of the old field
    if current_subdomain and current_subdomain not in ['www', 'gitanshuimpex']:
        if not product.category.subdomain or product.category.subdomain.prefix != current_subdomain:
            return redirect('home')

    return render(request, 'gipl_app/product_detail.html', {'product': product})

def global_presence(request):
    return render(request, 'gipl_app/global_presence.html')

def contact(request):
    # Detect subdomain for branding and lead tracking
    host = request.get_host().split('.')
    subdomain_val = host[0] if len(host) > 2 else 'Main'
    sub_info = Subdomain.objects.filter(prefix=subdomain_val).first() if subdomain_val != 'Main' else None

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # commit=False allows us to add the subdomain before saving to DB
            inquiry = form.save(commit=False)
            inquiry.source_subdomain = subdomain_val
            inquiry.save()

            # Simple Text Email
            subject = f"GIPL Inquiry - {subdomain_val.capitalize()}"
            message = (
                f"Dear {inquiry.name},\n\n"
                f"Thank you for reaching out to Gitanshu Impex Pvt. Ltd. regarding our {subdomain_val} products. "
                "We have received your inquiry and our export team will get back to you soon.\n\n"
                "Best regards,\n"
                "GIPL Team"
            )
            send_mail(subject, message, 'gitanshuimpex@gmail.com', [inquiry.email], fail_silently=False)
            
            messages.success(request, "Your inquiry has been submitted successfully!")
            return redirect(request.path)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InquiryForm()

    return render(request, 'gipl_app/contact.html', {
        'form': form,
        'sub_info': sub_info
    })

def global_inquiry(request):
    """
    Handles the inquiry form in the footer across all pages.
    Uses a professional HTML email template.
    """
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            
            # Identify source subdomain
            host = request.get_host().split('.')
            subdomain_val = host[0] if len(host) > 2 else 'Main'
            inquiry.source_subdomain = subdomain_val
            inquiry.save()

            # Prepare Professional HTML Email
            context = {
                'name': inquiry.name, 
                'year': datetime.now().year,
                'subdomain': subdomain_val.capitalize()
            }
            html_content = render_to_string('gipl_app/email.html', context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=f"Inquiry Received - GIPL {subdomain_val.capitalize()}",
                body=text_content,
                from_email='gitanshuimpex@gmail.com',
                to=[inquiry.email],
                cc=['guptajiten@gmail.com'] # Copying the director for visibility
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "Thank you! Our team will contact you shortly.")
            return redirect(request.path)
        else:
            messages.error(request, "Inquiry failed. Please check your details.")
    
    # If GET request, just redirect to the main contact page
    return redirect('contact')
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