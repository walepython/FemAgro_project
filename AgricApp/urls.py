
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path("crops/", views.crop_list, name="crop_list"),
    path("crop/<int:id>/", views.crop_detail, name="crop_detail"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),

    path('livestock/', views.livestock_list, name='livestock_list'),
    path('livestock/<int:id>/', views.livestock_detail, name='livestock_detail'),

    # path('products/', views.ProductsView.as_view(), name='products'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('search/',views.search,name='search'),
    path('guides/',views.guides,name='guides'),
    path('guides/<slug:slug>/',views.guide_detail,name='guide_detail'),
    path('farm-technology/',views.farm_technology,name='farm_technology'),
    path('farm-technology/<slug:slug>/',views.technology_detail,name='technology_detail'),

    # Category listing — slug matches the href values in navbar

    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('donate/',views.donation_page,name='donate'),
    path('donation/verify/',views.verify_payment,name='verify_payment'),
    path('paystack/webhook/',views.paystack_webhook,
    name='paystack_webhook'),
    path('paystack/callback/',views.paystack_callback,
    name='paystack_callback'),
    path('donate/success/',views.donation_success,    name='donation_success'),
    path('donate/failed/',views.donation_failed,     name='donation_failed'),
]