# FemAgro – Agricultural Information Platform

FemAgro is a Django-based agricultural information platform designed to provide farmers, agricultural enthusiasts and other users with useful farming resources, crop information, livestock management guidance and agricultural technology information.

The platform also provides user registration, agricultural articles, contact messaging, and an online donation system powered by Paystack.

## Features

### Agricultural information
- Agricultural categories and crop information.
- Crop details, including botanical names, planting methods, soil types, seasons and harvesting information.
- Livestock information, including breeds, feeding, housing, breeding and health management.
- Additional product and livestock image galleries.
- Farming guides and educational resources.
- Agricultural technology information.
- Practical farmer tips.

### Content management
- Django administration dashboard.
- Create, update and manage agricultural content.
- CKEditor 5 rich-text editing.
- Manage categories, products, livestock, guides, blog posts and testimonials.
- Upload and manage images.

### User functionality
- User registration.
- User login and logout.
- Agricultural content search.
- Category filtering.
- Crop filtering by season and soil type.
- Paginated category listings.
- Contact form and message management.

### Donation system
- Paystack payment initialization.
- Donation records and transaction references.
- Payment callback and webhook endpoints.
- Donation status tracking.
- Donation progress displayed on the homepage.
- Donor confirmation and administrator notification emails.

**Note:** The current code includes a monthly donation flag, but recurring subscription billing has not been verified.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django 6.0.3 | Backend web framework |
| SQLite | Development database |
| HTML | Page structure |
| CSS | Styling |
| JavaScript | Frontend interactions |
| CKEditor 5 | Rich-text editing |
| Pillow | Image processing |
| Paystack | Payment integration |
| Gmail SMTP | Email delivery |
| python-decouple | Environment variable configuration |
| Requests | HTTP communication with Paystack |

## Project Structure

```text
Agric_Farm/
│
├── Agric_Farm/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── AgricApp/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── urls.py
│   └── apps.py
│
├── template/
├── static/
├── media/
├── logs/
├── requirements.txt
├── manage.py
├── .env
├── .gitignore
├── README.md
└── DOCUMENTATION.md
```

*The structure above is a simplified overview. Your actual template and static directories may contain additional subdirectories.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/walepython/FemAgro_project.git
```

### 2. Enter the project directory

```bash
cd FemAgro_project
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root, alongside `manage.py`.

Add the following variables:

```env
SECRET_KEY=your_django_secret_key
PAYSTACK_PUBLIC_KEY=your_paystack_public_key
PAYSTACK_SECRET_KEY=your_paystack_secret_key
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

Replace the example values with your own credentials.

**Important:** Never commit `.env` or expose your secret keys in public repositories.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

The root URL redirects to `/farm/`.

## Application URLs

| URL | Purpose |
|---|---|
| `/` | Redirects to the agricultural homepage |
| `/farm/` | Homepage |
| `/farm/about/` | About page |
| `/farm/services/` | Services |
| `/farm/category/<slug>/` | Agricultural category |
| `/farm/crop/<id>/` | Crop details |
| `/farm/livestock/` | Livestock listings |
| `/farm/livestock/<id>/` | Livestock details |
| `/farm/blog/` | Blog |
| `/farm/guides/` | Farming guides |
| `/farm/farm-technology/` | Agricultural technology |
| `/farm/search/` | Search |
| `/farm/contact/` | Contact page |
| `/farm/signup/` | User registration |
| `/farm/login/` | User login |
| `/farm/logout/` | User logout |
| `/farm/donate/` | Donation page |
| `/admin/` | Django administration |
| `/ckeditor5/` | CKEditor 5 integration |

## Static Files and Uploaded Media

The project uses Django static files and media configuration.

Static files:

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

Uploaded media:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

During development, Django serves these files through the development URL configuration.

For production, configure a suitable static and media file serving solution.

## Payment Integration

FemAgro uses Paystack for donation payments.

The integration includes:
- Transaction initialization.
- Payment redirection.
- Payment verification.
- Paystack webhook processing.
- Donation status updates.
- Email notifications.

The application uses Nigerian Naira (NGN) for its donation transaction verification.

Before production deployment, ensure callback and manual verification validate the transaction reference, amount and currency, not just the transaction success status.

## Development Checks

Run Django's system checks:

```bash
python manage.py check
```

Check for missing model migrations:

```bash
python manage.py makemigrations --check
```

Apply migrations:

```bash
python manage.py migrate
```

## Production Deployment Considerations

Before deploying FemAgro:

1. Set `DEBUG=False`.
2. Configure `ALLOWED_HOSTS` with the actual domain.
3. Store all credentials in secure environment variables.
4. Use HTTPS.
5. Configure production static and media storage.
6. Review payment verification and webhook handling.
7. Configure an appropriate production database.
8. Configure logging and email delivery.
9. Run Django's deployment security checks.

Run:

```bash
python manage.py check --deploy
```

## Repository

GitHub: https://github.com/walepython/FemAgro_project

## License

Add your chosen open-source or proprietary license before distributing the project.