
from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    Category,
    Guide,
    Livestock,
    Product,
    ProductImage,
    FarmerTip,
    Service,
    BlogPost,
    Technology,
    Testimonial,
    ContactMessage,
    Donation,
)


# ==========================================
# CKEDITOR 5 ADMIN FORMS
# ==========================================


class ProductAdminForm(forms.ModelForm):
    season = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    soil_type = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    planting_method = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    water_requirement = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    germination_time = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    maturity_time = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    harvest_method = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    farming_tips = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    benefit = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )
    description = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name="default")
    )

    class Meta:
        model = Product
        fields = "__all__"




class LivestockAdminForm(forms.ModelForm):
    breed_types = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))
    housing = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))
    feeding = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))
    breeding = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))
    health_management = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))
    products = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))
    benefits = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))
    description = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = Livestock
        fields = "__all__"


class GuideAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = Guide
        fields = "__all__"


class TechnologyAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = Technology
        fields = "__all__"


class FarmerTipAdminForm(forms.ModelForm):
    content = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = FarmerTip
        fields = "__all__"


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(required=False, widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = BlogPost
        fields = "__all__"



# ==========================================
# IMAGE INLINES
# ==========================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fk_name = "product"
    extra = 3


class LivestockImageInline(admin.TabularInline):
    model = ProductImage
    fk_name = "livestock"
    extra = 3


# ==========================================
# CATEGORY ADMIN
# ==========================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


# ==========================================
# PRODUCT ADMIN
# ==========================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageInline]

    list_display = (
        "name",
        "category",
        "season",
        "soil_type",
        "maturity_time",
        "created_at",
    )

    list_filter = ("category", "season", "soil_type")
    search_fields = ("name", "soil_type", "season")
    ordering = ("-created_at",)


# ==========================================
# LIVESTOCK ADMIN
# ==========================================

@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    form = LivestockAdminForm
    inlines = [LivestockImageInline]

    list_display = (
        "name",
        "category",
        "feeding",
        "breeding",
        "created_at",
    )

    list_filter = ("category",)
    search_fields = ("name", "feeding", "breeding")
    ordering = ("-created_at",)


# ==========================================
# PRODUCT IMAGE ADMIN
# ==========================================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "livestock", "image")
    list_filter = ("product", "livestock")


# ==========================================
# FARMER TIP ADMIN
# ==========================================

@admin.register(FarmerTip)
class FarmerTipAdmin(admin.ModelAdmin):
    form = FarmerTipAdminForm
    list_display = ("title", "created_at")
    search_fields = ("title", "content")


# ==========================================
# SERVICE ADMIN
# ==========================================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "icon", "order"]
    list_editable = ["order"]


# ==========================================
# BLOG POST ADMIN
# ==========================================

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ["title", "created_at"]
    prepopulated_fields = {"slug": ("title",)}


# ==========================================
# GUIDE ADMIN
# ==========================================

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    form = GuideAdminForm
    list_display = ["title", "category", "created_at"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["category"]
    search_fields = ["title"]


# ==========================================
# TECHNOLOGY ADMIN
# ==========================================

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    form = TechnologyAdminForm
    list_display = ("title", "created_at")
    prepopulated_fields = {"slug": ("title",)}


# ==========================================
# TESTIMONIAL ADMIN
# ==========================================

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "rating", "created_at"]
    list_editable = ["rating"]
    ordering = ["-created_at"]


# ==========================================
# CONTACT MESSAGE ADMIN
# ==========================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "created_at", "is_read"]
    list_filter = ["is_read"]
    list_editable = ["is_read"]

    readonly_fields = [
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "created_at",
    ]


# ==========================================
# DONATION ADMIN
# ==========================================

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = [
        "donor_name",
        "email",
        "amount",
        "status",
        "monthly",
        "created_at",
    ]

    list_filter = ["status", "monthly", "anonymous"]
    search_fields = ["donor_name", "email", "reference"]
    readonly_fields = ["reference", "created_at"]
    ordering = ["-created_at"]
