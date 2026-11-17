# FemAgro – Technical Documentation

## 1. Project Overview

FemAgro is an agricultural information platform developed with Python and Django.

Its primary purpose is to provide structured agricultural information, including crop details, livestock management, farming guides, agricultural technologies and educational content.

The platform also includes user authentication, content management, contact messaging and an online donation workflow.

## 2. Technology Stack

| Component | Implementation |
|---|---|
| Programming language | Python |
| Backend framework | Django 6.0.3 |
| Database | SQLite |
| Frontend | HTML, CSS and JavaScript |
| Rich-text editor | django-ckeditor-5 |
| Image processing | Pillow |
| HTTP client | Requests |
| Payment provider | Paystack |
| Email service | Gmail SMTP |
| Environment configuration | python-decouple |

## 3. Application Architecture

The application follows Django's Model-View-Template (MVT) architecture.

### Model

Models define the database structure and represent the application's data.

Location:

```text
AgricApp/models.py
```

### View

Views contain the application logic. They retrieve data, process requests, validate submissions and return rendered pages.

Location:

```text
AgricApp/views.py
```

### Template

Templates provide the HTML presentation layer.

The project uses a project-level `template` directory and Django application templates.

### URL configuration

URL configurations connect incoming HTTP requests to their corresponding views.

Files:

```text
Agric_Farm/urls.py
AgricApp/urls.py
```

## 4. Database Models

The application defines twelve models.

### 4.1 Category

Stores agricultural categories.

Fields:
- `name`: Category name.
- `slug`: URL-friendly category identifier.
- `description`: Category description.

The slug is generated automatically from the category name when it is empty.

### 4.2 Guide

Stores agricultural educational guides.

Fields:
- `title`
- `slug`
- `short_description`
- `content`
- `image`
- `category`
- `created_at`

Relationship:

A Guide belongs to one Category. A Category can contain multiple Guides.

Guides are ordered by newest creation date.

### 4.3 Technology

Stores agricultural technology information.

Fields:
- `title`
- `slug`
- `short_description`
- `feature_1`
- `feature_2`
- `feature_3`
- `content`
- `image`
- `created_at`

The slug is generated from the title when not supplied.

### 4.4 Service

Stores services offered by the platform.

Fields:
- `icon`
- `title`
- `description`
- `order`

Services are ordered using the `order` field.

### 4.5 Product

Stores crop and agricultural product information.

Fields:
- `name`
- `botanical_name`
- `category`
- `season`
- `soil_type`
- `planting_method`
- `water_requirement`
- `germination_time`
- `maturity_time`
- `harvest_method`
- `farming_tips`
- `benefit`
- `description`
- `image`
- `created_at`

A Product belongs to one Category.

The model contains agricultural information to help users understand crop cultivation and management.

### 4.6 Livestock

Stores livestock information.

Fields:
- `name`
- `category`
- `breed_types`
- `housing`
- `feeding`
- `breeding`
- `health_management`
- `products`
- `benefits`
- `description`
- `image`
- `created_at`

A Livestock record belongs to one Category.

### 4.7 ProductImage

Stores additional images for products and livestock.

Fields:
- `product`
- `livestock`
- `image`

Both foreign keys are optional.

The model uses the `gallery` related name to access additional images from Product and Livestock instances.

### 4.8 FarmerTip

Stores practical farming tips.

Fields:
- `title`
- `content`
- `image`
- `created_at`

### 4.9 BlogPost

Stores agricultural articles and blog posts.

Fields:
- `title`
- `excerpt`
- `content`
- `image_url`
- `slug`
- `created_at`

Blog posts are ordered by newest creation date.

### 4.10 Testimonial

Stores testimonials.

Fields:
- `name`
- `role`
- `message`
- `rating`
- `image_url`
- `created_at`

The default rating is 5.

### 4.11 ContactMessage

Stores messages submitted through the contact form.

Fields:
- `name`
- `email`
- `phone`
- `subject`
- `message`
- `created_at`
- `is_read`

The `is_read` field helps administrators track messages that have been reviewed.

### 4.12 Donation

Stores donation and transaction information.

Fields:
- `donor_name`
- `email`
- `amount`
- `anonymous`
- `monthly`
- `reference`
- `status`
- `created_at`

Donation status choices:

| Status | Meaning |
|---|---|
| pending | Payment has not been confirmed |
| paid | Payment has been confirmed |
| failed | Payment failed |

The transaction reference is unique.

The `amount_display` property formats the donation amount as Nigerian Naira.

**Important:** The `monthly` field stores a monthly-donation selection. A recurring Paystack subscription implementation has not been established by the supplied code.

## 5. Database Relationships

The principal relationships are:

```text
Category
   |
   |----< Guide
   |
   |----< Product
   |
   |----< Livestock


Product
   |
   |----< ProductImage


Livestock
   |
   |----< ProductImage
```

The `Category` model has one-to-many relationships with Guide, Product and Livestock.

The `ProductImage` model can reference either a Product or Livestock record.

The other models do not declare foreign-key relationships in the supplied models file.

## 6. Application URL Structure

The main project URL configuration is located in:

```text
Agric_Farm/urls.py
```

It provides:
- Root redirection to `/farm/`.
- Django administration at `/admin/`.
- Application routes under `/farm/`.
- CKEditor 5 routes under `/ckeditor5/`.

### Application routes

| Route | View | Purpose |
|---|---|---|
| `/farm/` | `home` | Homepage |
| `/farm/crop/<id>/` | `crop_detail` | Crop information |
| `/farm/about/` | `AboutView` | About page |
| `/farm/services/` | `ServicesView` | Services |
| `/farm/livestock/` | `livestock_list` | Livestock listings |
| `/farm/livestock/<id>/` | `livestock_detail` | Livestock details |
| `/farm/blog/` | `blog_list` | Blog listing |
| `/farm/blog/<slug>/` | `blog_detail` | Blog details |
| `/farm/contact/` | `ContactView` | Contact form |
| `/farm/search/` | `search` | Search functionality |
| `/farm/guides/` | `guides` | Farming guides |
| `/farm/guides/<slug>/` | `guide_detail` | Guide details |
| `/farm/farm-technology/` | `farm_technology` | Technology listing |
| `/farm/farm-technology/<slug>/` | `technology_detail` | Technology details |
| `/farm/category/<slug>/` | `category_list` | Category listings |
| `/farm/login/` | `login_view` | User login |
| `/farm/signup/` | `signup_view` | User registration |
| `/farm/logout/` | `logout_view` | User logout |
| `/farm/donate/` | `donation_page` | Donation form |
| `/farm/donation/verify/` | `verify_payment` | Manual payment verification |
| `/farm/paystack/webhook/` | `paystack_webhook` | Paystack webhook |
| `/farm/paystack/callback/` | `paystack_callback` | Payment callback |
| `/farm/donate/success/` | `donation_success` | Donation success page |
| `/farm/donate/failed/` | `donation_failed` | Donation failure page |

## 7. Application Views and Business Logic

The main application logic is in `AgricApp/views.py`.

### Homepage

The homepage retrieves:
- Recently added products.
- Recent testimonials.
- Recent blog posts.
- Paid donations.
- Agricultural category counts.
- Donation totals and progress.

### Category listing

The category listing view:
- Retrieves a category using its slug.
- Retrieves products and livestock associated with that category.
- Supports text search.
- Supports season filtering.
- Supports soil filtering.
- Paginates crop results at twelve items per page.

### Search

The search view searches product and livestock names and descriptions.

### Crop and livestock details

The detail views retrieve individual records and their additional gallery images.

### Guides and technology

The application provides listing and detail views for farming guides and agricultural technology.

### Authentication

The project uses Django's built-in User model and authentication framework.

The custom registration form collects:
- First name.
- Last name.
- Username.
- Email.
- Password.
- Password confirmation.

Successful registration automatically logs the user in.

### Contact messaging

The ContactForm is a ModelForm based on ContactMessage.

Submitted messages are saved to the database and administrators can review them in Django administration.

## 8. Forms

Forms are defined in:

```text
AgricApp/forms.py
```

### ContactForm

A ModelForm connected to ContactMessage.

It collects the user's name, email, phone number, subject and message.

### CustomUserCreationForm

Extends Django's UserCreationForm.

It adds email, first name and last name fields while retaining Django's password validation.

### DonationForm

Handles donation input and validation.

The supplied code includes donor information, email, amount, anonymous selection and monthly selection.

The donation amount is configured with a minimum of ₦100 and a maximum of ₦10,000,000.

## 9. Django Administration

The administration configuration is defined in:

```text
AgricApp/admin.py
```

The following models are registered:

- Category
- Product
- Livestock
- ProductImage
- FarmerTip
- Service
- BlogPost
- Guide
- Technology
- Testimonial
- ContactMessage
- Donation

### CKEditor 5

Custom ModelForms use CKEditor5Widget to provide rich-text editing for agricultural content.

The editor is configured in `settings.py`.

### Image inlines

ProductImageInline allows additional product images to be managed from the Product administration page.

LivestockImageInline allows additional livestock images to be managed from the Livestock administration page.

### Administration features

The admin configuration includes:
- Search fields.
- List displays.
- Filters.
- Ordering.
- Editable service ordering.
- Editable testimonial ratings.
- Contact message read-status management.
- Read-only donation transaction references.

## 10. Paystack Donation Integration

The donation workflow is implemented in `AgricApp/views.py`.

### Donation initialization

1. A visitor opens the donation page.
2. The visitor submits the donation form.
3. The application validates the submitted information.
4. A pending Donation record is created.
5. A unique transaction reference is generated.
6. The application sends a transaction initialization request to Paystack.
7. The visitor is redirected to Paystack's authorization URL.

The application sends the donation amount in kobo, as required by Paystack's transaction API.

### Payment callback

After payment, Paystack redirects the visitor to the configured callback URL.

The callback requests transaction verification from Paystack.

The current callback implementation checks the returned transaction success status before updating the donation record.

### Webhook

The webhook endpoint:
- Accepts POST requests.
- Reads the `X-Paystack-Signature` header.
- Computes an HMAC SHA512 signature.
- Compares the calculated signature with the supplied signature.
- Processes successful charge events.
- Checks transaction reference, status, amount and NGN currency.
- Updates the donation status.
- Sends donor and administrator emails.

### Donation reporting

The homepage calculates the total of donations whose status is `paid`.

The configured donation goal is ₦1,000,000.

The progress percentage is capped at 100%.

### Payment security improvement required

The manual verification view and callback should both use the stronger transaction validation logic that checks:
- Transaction success status.
- Exact transaction reference.
- Expected amount.
- NGN currency.

The existing `verify_paystack_transaction()` helper contains these checks, but the supplied callback and manual verification implementations do not currently call it.

The donation status must only be updated after successful verification of all required transaction details.

Also, the `monthly` field should not be presented as proof of recurring billing until a Paystack subscription or recurring-charge workflow is implemented.

## 11. Email Configuration

The project uses Gmail SMTP.

Configuration is stored in `Agric_Farm/settings.py`.

The required environment variables are:

```env
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

The system uses email for:
- Donor confirmation.
- Administrator donation notifications.

Email delivery is configured to fail silently in the donation notification helpers, with errors logged when exceptions occur.

## 12. Static Files and Media

Static files:

```text
static/
```

Uploaded media:

```text
media/
```

Django settings define:
- `STATIC_URL`
- `STATIC_ROOT`
- `STATICFILES_DIRS`
- `MEDIA_URL`
- `MEDIA_ROOT`

Image fields use separate upload directories for products, livestock, guides, technology and farmer tips.

For production, configure persistent media storage and an appropriate static file serving mechanism.

## 13. Environment Variables

The project uses python-decouple to read sensitive settings.

Required variables:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django cryptographic secret |
| `PAYSTACK_PUBLIC_KEY` | Paystack public key |
| `PAYSTACK_SECRET_KEY` | Paystack secret key |
| `EMAIL_HOST_USER` | Gmail account |
| `EMAIL_HOST_PASSWORD` | Gmail app password |

Keep the `.env` file outside version control.

## 14. Logging and Error Handling

The application configures logging for errors originating from `AgricApp.views`.

The configured file destination is:

```text
logs/donation_errors.log
```

The project also has a console logging handler.

Ensure the `logs` directory exists in environments where the file handler is used.

## 15. Security Considerations

The application includes several security-related measures:
- Environment-based secret configuration.
- Django password validation.
- CSRF middleware.
- HTTP-only session cookies.
- HTTP-only CSRF cookies.
- Clickjacking protection.
- Paystack webhook signature verification.
- Donation submission rate limiting.
- Duplicate donation submission checks.

### Production improvements

Before deployment:
1. Disable Django DEBUG mode.
2. Configure specific allowed hostnames.
3. Enforce HTTPS.
4. Review cookie security settings.
5. Strengthen transaction callback verification.
6. Use a production-ready cache for rate limiting.
7. Review forwarded client IP handling behind proxies.
8. Configure production database and backups.
9. Configure secure static and media hosting.
10. Run Django deployment checks.

The current development configuration uses SQLite, `DEBUG=True` and `ALLOWED_HOSTS=["*"]`; these should not be copied unchanged into production.

## 16. Running the Project

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

Run the application:

```bash
python manage.py runserver
```

Run system checks:

```bash
python manage.py check
```

Check migration state:

```bash
python manage.py showmigrations
```

## 17. Future Development Opportunities

Potential future improvements include:
- Recurring donation subscriptions.
- More comprehensive payment reconciliation.
- Agricultural weather information.
- Improved crop recommendation features.
- Dedicated API endpoints for mobile applications.
- User profiles and saved farming resources.
- More advanced agricultural search and filtering.
- Production database migration and deployment automation.

## 18. Repository

GitHub:

https://github.com/walepython/FemAgro_project

---

**Documentation status:** Prepared from the supplied project configuration, models, views, forms, administration and URL configuration. Verify any future code changes against this document before treating it as a complete record of the application.