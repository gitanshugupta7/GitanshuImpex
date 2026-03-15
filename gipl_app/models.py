from django.db import models
from django.utils.text import slugify

class Subdomain(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., Industrial Tools")
    prefix = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="e.g., 'industrial' for industrial.gitanshuimpex.com"
    )
    is_active = models.BooleanField(default=True)
    
    # Professional Touch: Subdomain-specific Branding
    hero_title = models.CharField(max_length=200, blank=True, null=True)
    hero_subtitle = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.prefix}.gitanshuimpex.com"

class ProductCategory(models.Model):
    # Link multiple categories to one subdomain
    subdomain = models.ForeignKey(
        Subdomain, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Optional: Auto-generate subdomain from name if left blank
        if not self.subdomain_prefix:
            self.subdomain_prefix = slugify(self.name).replace("-", "") 
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    specs = models.TextField(blank=True)
    moq = models.CharField(max_length=50, blank=True, null=True)
    packaging = models.CharField(max_length=100, blank=True, null=True)
    exported_to = models.CharField(max_length=200, blank=True, null=True)
    features = models.JSONField(default=list, blank=True)  # e.g. ["Smooth Writing", "ISO Certified"]
    attributes = models.JSONField(default=dict, blank=True)  # e.g. {"Ink Color": "Blue", "Tip Size": "0.7mm"}

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=150)
    comment = models.TextField()
    image = models.ImageField(upload_to='testimonials/')

    def __str__(self):
        return self.name

# Model for the common Contact/Inquiries form ("Let's Do Business Together")
class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=10)  # New field
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name} on {self.created_at.strftime('%Y-%m-%d')}"


class CarouselItem(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    cta_text = models.CharField(max_length=50, blank=True, null=True)
    cta_link = models.URLField(blank=True, null=True)
    desktop_image = models.ImageField(upload_to='carousel/desktop/')
    mobile_image = models.ImageField(upload_to='carousel/mobile/')

    def __str__(self):
        return self.title