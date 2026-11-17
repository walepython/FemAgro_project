from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from .models import FarmerTip, Guide, Livestock, ProductImage, Service, Product, Technology, Testimonial, BlogPost,Category, Donation
from .forms import ContactForm, CustomUserCreationForm, DonationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from requests.exceptions import ConnectionError, Timeout, RequestException

from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
import json
from django.db.models import Sum
import uuid
import requests
import hashlib
import hmac
import logging
from django.urls import reverse
# Create your views here.

def home(request):
    goal = 1000000
    total = _get_total()
    percentage = min((total / goal) * 100, 100)

    featured_products = Product.objects.all().order_by('-created_at')[:4]
    testimony = Testimonial.objects.all().order_by('-created_at')[:3]
    blog_posts = BlogPost.objects.all().order_by('-created_at')[:3]

    supporters = (
        Donation.objects
        .filter(status='paid')
        .order_by('-created_at')[:6]
    )

    return render(request, 'home.html', {
        'annual_count': Product.objects.filter(
            category__slug='annual-crops'
        ).count(),

        'cash_count': Product.objects.filter(
            category__slug='cash-crops'
        ).count(),

        'livestock_count': Livestock.objects.filter(
            category__slug='livestock'
        ).count(),

        'veg_count': Product.objects.filter(
            category__slug='vegetables'
        ).count(),

        'fruit_count': Product.objects.filter(
            category__slug='fruits'
        ).count(),

        'tree_count': Product.objects.filter(
            category__slug='tree-crops'
        ).count(),

        'poultry_count': Livestock.objects.filter(
            category__slug='poultry'
        ).count(),

        'aqua_count': Product.objects.filter(
            category__slug='aquaculture'
        ).count(),

        'featured_products': featured_products,
        'testimonials': testimony,
        'blog_posts': blog_posts,

        'total': total,
        'goal': goal,
        'percentage': percentage,
        'supporters': supporters,
    })


# def modern_farming_technology(request):
#     return render(request, 'farming_technology.html')


def crop_list(request):
    crops = Product.objects.all()

    season = request.GET.get('season')
    soil = request.GET.get('soil')

    if season:
        crops = crops.filter(season__icontains=season)

    if soil:
        crops = crops.filter(soil_type__icontains=soil)

    context = {
        "crops": crops
    }

    return render(request, "crop_list.html", context)

def livestock_list(request):
    livestock = Livestock.objects.all()
    return render(request, "livestock_list.html", {"livestock": livestock})

def livestock_detail(request, id):
    animal = get_object_or_404(Livestock, id=id)
    images = ProductImage.objects.filter(livestock=animal)
    return render(request, "livestock_detail.html", {"animal": animal,"image":images})

def crop_detail(request, id):
    crop = get_object_or_404(Product, id=id)
    images = ProductImage.objects.filter(product=crop)
    print(images)
    return render(request, "crop_detail.html", {"crop": crop,"image":images})


# def category_list(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     products = Product.objects.filter(category=category)
#     return render(request, 'category_list.html', {
#         'category': category,
#         'products': products,
#         'active_category': slug,   # <-- this highlights the active tab
#     })

def category_list(request, slug):

    category = get_object_or_404(Category, slug=slug)

    # Start with all products in this category
    crops = Product.objects.filter(category=category).order_by('name')
    livestock = Livestock.objects.filter(category=category)

    # ── Text search ──────────────────────────────────────────
    q = request.GET.get('q', '').strip()
    if q:
        crops = crops.filter(
            Q(name__icontains=q) |
            Q(botanical_name__icontains=q) |
            Q(description__icontains=q)
        )

    # ── Season filter ─────────────────────────────────────────
    season = request.GET.get('season', '').strip()
    if season:
        crops = crops.filter(season__icontains=season)

    # ── Soil filter ───────────────────────────────────────────
    soil = request.GET.get('soil', '').strip()
    if soil:
        crops = crops.filter(soil_type__icontains=soil)

    # ── Pagination ────────────────────────────────────────────
    paginator = Paginator(crops, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'category_list.html', {
        'category': category,
        'livestock': livestock,
        'crops': page_obj,
        'active_category': slug,
        'q': q,
        'selected_season': season,
        'selected_soil': soil,
    })



def search(request):
    q = request.GET.get('q', '').strip()

    products   = []
    livestock  = []
    aquaculture = []

    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).select_related('category')

        livestock   = Livestock.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).select_related('category')

        aquaculture = Livestock.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).select_related('category')

    total = len(products) + len(livestock) + len(aquaculture)

    return render(request, 'search.html', {
        'query':      q,
        'products':   products,
        'livestock':  livestock,
        'aquaculture': aquaculture,
        'total':      total,
    })


def tips_list(request):
    tips = FarmerTip.objects.all().order_by("-created_at")
    return render(request, "tips.html", {"tips": tips})

# You could later integrate weather APIs like:
#OpenWeather API
#WeatherStack API
def recommended_crops(season):
    if season == "rainy":
        return Product.objects.filter(season__icontains="rainy")
    else:
        return Product.objects.filter(season__icontains="dry")

def crop_recommendation(request):

    soil = request.GET.get("soil")

    crops = Product.objects.filter(soil_type__icontains=soil)

    return render(request, "recommendation.html", {
        "crops": crops,
        "soil": soil
    })

def blog_list(request):

    featured_post = BlogPost.objects.first()

    recent_posts = BlogPost.objects.exclude(
        id=featured_post.id
    )[:6] if featured_post else BlogPost.objects.all()[:6]

    context = {
        'featured_post': featured_post,
        'recent_posts': recent_posts,
    }

    return render(request, 'blog.html', context)


def blog_detail(request, slug):

    post = get_object_or_404(BlogPost, slug=slug)

    related_posts = BlogPost.objects.exclude(
        id=post.id
    )[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
    }

    return render(request, 'blog_detail.html', context)

class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)


class ServicesView(TemplateView):
    template_name = 'services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

def guides(request):
    cat_slug = request.GET.get('cat', '')

    all_guides = Guide.objects.select_related('category').all()

    if cat_slug:
        all_guides = all_guides.filter(category__slug=cat_slug)

    featured   = Guide.objects.select_related('category').first()
    categories = Category.objects.all()

    return render(request, 'guide.html', {
        'guides':     all_guides,
        'featured':   featured,
        'categories': categories,
        'active_cat': cat_slug,
        'total':      Guide.objects.count(),
    })

def guide_detail(request, slug):
    guide      = get_object_or_404(Guide, slug=slug)
    more       = Guide.objects.exclude(slug=slug)\
                              .filter(category=guide.category)[:3]
    return render(request, 'guide_details.html', {
        'guide': guide,
        'more':  more,
    })

def farm_technology(request):
    technologies = Technology.objects.all()

     # Debug prints
    print(f"Number of technologies: {technologies.count()}")
    for tech in technologies:
        print(f"Tech: {tech.title}, Image exists: {bool(tech.image)}")
        print(f"Image URL: {tech.image.url if tech.image else 'No image'}")


    context = {
        'technologies': technologies
    }

    return render( request, 'farming_technology.html', context
    )

def technology_detail(request, slug):
    technology = get_object_or_404(Technology, slug=slug)

    related = Technology.objects.exclude(id=technology.id)[:3]

    return render( request,'farm_tech_detail.html',
        {
            'technology': technology,
            'related': related
        }
    )

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect( 'home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

logger = logging.getLogger(__name__)


# ── Rate limiting helper ───────────────────────────
def is_rate_limited(ip, limit=5, window=300):
    """
    Block IP if it submits more than `limit`
    donations within `window` seconds.
    """
    key   = f'donate_ratelimit_{ip}'
    count = cache.get(key, 0)

    if count >= limit:
        return True

    cache.set(key, count + 1, timeout=window)
    return False


# ── Get real IP ────────────────────────────────────
def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


# ── Send confirmation email ────────────────────────
def send_donation_confirmation(donation):
    try:
        send_mail(
            subject = '🌱 Thank you for supporting AgriLearn!',
            message = f"""
Dear {donation.donor_name or 'Supporter'},

Thank you for your generous donation of ₦{donation.amount:,.2f} to AgriLearn.

Your support helps us create free farming guides and educational
resources for smallholder farmers across Africa.

Donation Reference: {donation.reference}
Amount: ₦{donation.amount:,.2f}
{'Monthly donation — you will be charged monthly.' if donation.monthly else ''}

With gratitude,
The AgriLearn Team
            """.strip(),
            from_email    = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [donation.email],
            fail_silently  = True,
        )
    except Exception as e:
        logger.error(f'Failed to send confirmation email: {e}')


# ── Send admin notification ────────────────────────
def send_admin_notification(donation):
    try:
        send_mail(
            subject = f'New Donation: ₦{donation.amount:,.2f} from {donation.email}',
            message = f"""
New donation received on FemAgro:

Name:      {donation.donor_name or 'Anonymous'}
Email:     {donation.email}
Amount:    ₦{donation.amount:,.2f}
Monthly:   {'Yes' if donation.monthly else 'No'}
Anonymous: {'Yes' if donation.anonymous else 'No'}
Reference: {donation.reference}
Time:      {donation.created_at}
            """.strip(),
            from_email    = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.EMAIL_HOST_USER],
            fail_silently  = True,
        )
    except Exception as e:
        logger.error(f'Failed to send admin notification: {e}')


# ── Main donation view ─────────────────────────────
def donation_page(request):

    if request.method == 'POST':

        # ── Rate limit check ───────────────────
        ip = get_client_ip(request)
        if is_rate_limited(ip):
            form = DonationForm()
            return render(request, 'donate.html', {
                'form':        form,
                'rate_limited': True,
                'total':       _get_total(),
                'goal':        1000000,
                'percentage':  _get_percentage(),
            })

        form = DonationForm(request.POST)

        if form.is_valid():

            # Check duplicate submission (same email + amount
            # within last 60 seconds)
            email  = form.cleaned_data['email']
            amount = form.cleaned_data['amount']

            recent = Donation.objects.filter(
                email      = email,
                amount     = amount,
                created_at__gte = timezone.now() - timezone.timedelta(seconds=60)
            ).exists()

            if recent:
                form.add_error(
                    None,
                    'It looks like you already submitted this donation. '
                    'Please wait a moment before trying again.'
                )
                return render(request, 'donate.html', {
                    'form':       form,
                    'total':      _get_total(),
                    'goal':       1000000,
                    'percentage': _get_percentage(),
                })

            # Create donation record (pending)
            donation = Donation.objects.create(
                donor_name = form.cleaned_data['donor_name'],
                email      = email,
                amount     = amount,
                anonymous  = form.cleaned_data['anonymous'],
                monthly    = form.cleaned_data['monthly'],
                reference  = str(uuid.uuid4()).replace('-', '')[:20],
            )

            # ── Call Paystack ──────────────────
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type':  'application/json',
            }

            data = {
                'email':        donation.email,
                'amount':       int(donation.amount * 100),
                'reference':    donation.reference,
                'callback_url': request.build_absolute_uri(
                    reverse('paystack_callback')
                ),
                'metadata': {
                    'donor_name': donation.donor_name,
                    'monthly':    donation.monthly,
                    'anonymous':  donation.anonymous,
                }
            }

            try:
                response = requests.post(
                    'https://api.paystack.co/transaction/initialize',
                    json    = data,
                    headers = headers,
                    timeout = 15,
                )
                response_data = response.json()

                if response_data.get('status'):
                    return redirect(
                        response_data['data']['authorization_url']
                    )
                else:
                    logger.error(
                        f'Paystack init failed: {response_data}'
                    )
                    form.add_error(
                        None,
                        f"Payment error: {response_data.get('message', 'Please try again.')}"
                    )

            except ConnectionError:
                logger.error('Paystack connection failed — no internet')
                form.add_error(
                    None,
                    'Could not connect to payment provider. '
                    'Please check your internet and try again, '
                    'or donate via bank transfer below.'
                )

            except Timeout:
                logger.error('Paystack request timed out')
                form.add_error(
                    None,
                    'Payment provider timed out. Please try again.'
                )

            except RequestException as e:
                logger.error(f'Paystack request error: {e}')
                form.add_error(None, 'Payment error. Please try again.')

    else:
        form = DonationForm()

    return render(request, 'donate.html', {
        'form':       form,
        'total':      _get_total(),
        'goal':       1000000,
        'percentage': _get_percentage(),
    })

# ── Verify view (optional manual check) ───────────
def verify_payment(request):
    reference = request.GET.get('reference', '')

    if not reference:
        return redirect('donation_failed')

    try:
        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'
            },
            timeout=15,
        )
        result = response.json()

        if (result.get('status') and
                result['data']['status'] == 'success'):

            donation = Donation.objects.get(reference=reference)
            donation.status = 'paid'
            donation.save()

            return render(request, 'donation_success.html', {
                'donation': donation
            })

    except Exception as e:
        logger.error(f'Verify error: {e}')

    return render(request, 'donation_failed.html')



# ── Webhook (Paystack server-to-server backup) ─────

@csrf_exempt
@require_POST
def paystack_webhook(request):

    # Verify Paystack signature
    paystack_signature = request.headers.get(
        'X-Paystack-Signature', ''
    )

    secret = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
    body = request.body

    expected_sig = hmac.new(
        secret,
        body,
        hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(
        expected_sig,
        paystack_signature
    ):
        logger.warning('Webhook: invalid signature')
        return HttpResponse(status=400)

    try:
        payload = json.loads(body)
        event = payload.get('event')
        reference = payload.get('data', {}).get('reference')

        if event == 'charge.success' and reference:

            donation = Donation.objects.filter(
                reference=reference
            ).first()

            if donation:
                transaction = payload.get('data', {})

                expected_amount = int(donation.amount * 100)

                valid_payment = (
                    transaction.get('status') == 'success'
                    and transaction.get('reference') == donation.reference
                    and transaction.get('amount') == expected_amount
                    and transaction.get('currency') == 'NGN'
                )

                if valid_payment and donation.status != 'paid':
                    donation.status = 'paid'
                    donation.save(update_fields=['status'])

                    send_donation_confirmation(donation)
                    send_admin_notification(donation)

                    logger.info(
                        f'Webhook: donation {reference} marked paid'
                    )

    except Exception as e:
        logger.error(f'Webhook error: {e}')

    return HttpResponse(status=200)



# ── Paystack callback (user returns after payment) ─
def paystack_callback(request):
    reference = request.GET.get('reference', '')

    if not reference:
        return redirect('donation_failed')

    # Verify with Paystack
    try:
        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'
            },
            timeout = 15,
        )
        data = response.json()

        if (data.get('status') and
                data['data']['status'] == 'success'):

            try:
                donation = Donation.objects.get(reference=reference)

                if donation.status != 'paid':
                    donation.status = 'paid'
                    donation.save()

                    # Send emails
                    send_donation_confirmation(donation)
                    send_admin_notification(donation)

                return redirect('donation_success')

            except Donation.DoesNotExist:
                logger.error(
                    f'Callback: donation not found ref={reference}'
                )
                return redirect('donation_failed')

    except Exception as e:
        logger.error(f'Callback verification error: {e}')

    return redirect('donation_failed')



def donation_success(request):
    return render(request, 'donation_success.html')

def donation_failed(request):
    return render(request, 'donation_failed.html')

def _get_total():
    return Donation.objects.filter(
        status='paid'
    ).aggregate(Sum('amount'))['amount__sum'] or 0


def _get_percentage():
    total = _get_total()
    goal  = 1000000
    return min((total / goal) * 100, 100)


from decimal import Decimal
import requests

def verify_paystack_transaction(reference, donation):
    try:
        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers={
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'
            },
            timeout=15
        )

        response.raise_for_status()
        result = response.json()

        if not result.get('status'):
            return False

        transaction = result.get('data', {})

        expected_amount = int(donation.amount * 100)

        return (
            transaction.get('status') == 'success'
            and transaction.get('reference') == donation.reference
            and transaction.get('amount') == expected_amount
            and transaction.get('currency') == 'NGN'
        )

    except requests.RequestException as error:
        logger.error(
            f'Paystack verification error: {error}'
        )
        return False
