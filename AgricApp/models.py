from django.db import models

from django.utils.text import slugify
import uuid
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField( blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Guide(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)

    short_description = models.TextField()

    content = models.TextField()

    image = models.ImageField(
        upload_to='guides/',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='guides'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Technology(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    short_description = models.TextField()

    feature_1 = models.CharField(max_length=255)
    feature_2 = models.CharField(max_length=255)
    feature_3 = models.CharField(max_length=255)

    content = models.TextField()

    image = models.ImageField(upload_to='technology/')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Service(models.Model):
    icon = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    botanical_name = models.CharField(max_length=100,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    season = models.TextField(blank=True)
    soil_type = models.TextField(blank=True)
    planting_method = models.TextField(blank=True)
    water_requirement = models.TextField(blank=True)
    germination_time = models.TextField(blank=True)
    maturity_time = models.TextField(blank=True)
    harvest_method = models.TextField(blank=True)
    farming_tips = models.TextField(blank=True)
    benefit = models.TextField(blank=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Livestock(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    breed_types = models.TextField(blank=True)
    housing = models.TextField(blank=True)
    feeding = models.TextField(blank=True)
    breeding = models.TextField(blank=True)
    health_management = models.TextField(blank=True)

    products = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='livestock/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery",
        null=True,
        blank=True
    )
    livestock = models.ForeignKey(
        Livestock,
        on_delete=models.CASCADE,
        related_name="gallery",
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        if self.product:
            return f"Product Image - {self.product.name}"
        elif self.livestock:
            return f"Livestock Image - {self.livestock.name}"
        return "Image"

class FarmerTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="tips/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    excerpt = models.TextField()
    content = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    slug = models.SlugField(unique=True, max_length=300,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Donation(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    donor_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    anonymous = models.BooleanField(default=False)
    monthly = models.BooleanField(default=False)
    reference = models.CharField(max_length=100, unique=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation - {self.reference}"

    @property
    def amount_display(self):
        return f"₦{self.amount:,.2f}"