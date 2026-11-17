
from decimal import Decimal
from unittest.mock import patch, Mock

from django.test import TestCase, Client
from django.urls import reverse

from .models import Donation
from .views import verify_paystack_transaction


class PaystackVerificationTests(TestCase):

    def setUp(self):
        self.donation = Donation.objects.create(
            donor_name="Test Donor",
            email="test@example.com",
            amount=Decimal("5000.00"),
            anonymous=False,
            monthly=False,
            reference="FEMAGRO-TEST-001",
            status="pending"
        )

    def make_paystack_response(
        self,
        reference="FEMAGRO-TEST-001",
        amount=500000,
        currency="NGN",
        status="success"
    ):
        response = Mock()
        response.json.return_value = {
            "status": True,
            "data": {
                "status": status,
                "reference": reference,
                "amount": amount,
                "currency": currency
            }
        }
        response.raise_for_status.return_value = None
        return response

    @patch("AgricApp.views.requests.get")
    def test_successful_payment_verification(self, mock_get):
        mock_get.return_value = self.make_paystack_response()

        result = verify_paystack_transaction(
            self.donation.reference,
            self.donation
        )

        self.assertTrue(result)

    @patch("AgricApp.views.requests.get")
    def test_wrong_reference_is_rejected(self, mock_get):
        mock_get.return_value = self.make_paystack_response(
            reference="WRONG-REFERENCE"
        )

        result = verify_paystack_transaction(
            self.donation.reference,
            self.donation
        )

        self.assertFalse(result)

    @patch("AgricApp.views.requests.get")
    def test_wrong_amount_is_rejected(self, mock_get):
        mock_get.return_value = self.make_paystack_response(
            amount=100000
        )

        result = verify_paystack_transaction(
            self.donation.reference,
            self.donation
        )

        self.assertFalse(result)

    @patch("AgricApp.views.requests.get")
    def test_wrong_currency_is_rejected(self, mock_get):
        mock_get.return_value = self.make_paystack_response(
            currency="USD"
        )

        result = verify_paystack_transaction(
            self.donation.reference,
            self.donation
        )

        self.assertFalse(result)

    @patch("AgricApp.views.requests.get")
    def test_failed_transaction_is_rejected(self, mock_get):
        mock_get.return_value = self.make_paystack_response(
            status="failed"
        )

        result = verify_paystack_transaction(
            self.donation.reference,
            self.donation
        )

        self.assertFalse(result)

    @patch("AgricApp.views.requests.get")
    def test_paystack_connection_error(self, mock_get):
        import requests

        mock_get.side_effect = requests.ConnectionError(
            "Connection unavailable"
        )

        result = verify_paystack_transaction(
            self.donation.reference,
            self.donation
        )

        self.assertFalse(result)

    @patch("AgricApp.views.requests.get")
    def test_different_local_reference_is_rejected(self, mock_get):
        result = verify_paystack_transaction(
            "ANOTHER-REFERENCE",
            self.donation
        )

        self.assertFalse(result)
        mock_get.assert_not_called()



import json
import hashlib
import hmac

from django.conf import settings
from django.urls import reverse


class PaystackCallbackTests(TestCase):

    def setUp(self):
        self.donation = Donation.objects.create(
            donor_name="Test Donor",
            email="test@example.com",
            amount=Decimal("5000.00"),
            anonymous=False,
            monthly=False,
            reference="FEMAGRO-CALLBACK-001",
            status="pending"
        )

    def make_response(self, status="success", amount=500000):
        response = Mock()
        response.json.return_value = {
            "status": True,
            "data": {
                "status": status,
                "reference": self.donation.reference,
                "amount": amount,
                "currency": "NGN"
            }
        }
        response.raise_for_status.return_value = None
        return response

    @patch("AgricApp.views.send_donation_confirmation")
    @patch("AgricApp.views.send_admin_notification")
    @patch("AgricApp.views.requests.get")
    def test_successful_callback_marks_donation_paid(
        self, mock_get, mock_admin_email, mock_donor_email
    ):
        mock_get.return_value = self.make_response()

        response = self.client.get(
            reverse("paystack_callback"),
            {"reference": self.donation.reference}
        )

        self.donation.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.donation.status, "paid")
        mock_donor_email.assert_called_once()
        mock_admin_email.assert_called_once()

    @patch("AgricApp.views.send_donation_confirmation")
    @patch("AgricApp.views.send_admin_notification")
    @patch("AgricApp.views.requests.get")
    def test_invalid_amount_does_not_mark_donation_paid(
        self, mock_get, mock_admin_email, mock_donor_email
    ):
        mock_get.return_value = self.make_response(amount=100000)

        self.client.get(
            reverse("paystack_callback"),
            {"reference": self.donation.reference}
        )

        self.donation.refresh_from_db()

        self.assertEqual(self.donation.status, "pending")
        mock_donor_email.assert_not_called()
        mock_admin_email.assert_not_called()

    @patch("AgricApp.views.send_donation_confirmation")
    @patch("AgricApp.views.send_admin_notification")
    @patch("AgricApp.views.requests.get")
    def test_repeated_callback_does_not_send_duplicate_emails(
        self, mock_get, mock_admin_email, mock_donor_email
    ):
        mock_get.return_value = self.make_response()

        callback_url = reverse("paystack_callback")
        callback_data = {"reference": self.donation.reference}

        self.client.get(callback_url, callback_data)
        self.client.get(callback_url, callback_data)

        self.donation.refresh_from_db()

        self.assertEqual(self.donation.status, "paid")
        self.assertEqual(mock_donor_email.call_count, 1)
        self.assertEqual(mock_admin_email.call_count, 1)


class PaystackWebhookTests(TestCase):

    def setUp(self):
        self.donation = Donation.objects.create(
            donor_name="Webhook Donor",
            email="webhook@example.com",
            amount=Decimal("5000.00"),
            anonymous=False,
            monthly=False,
            reference="FEMAGRO-WEBHOOK-001",
            status="pending"
        )

    def test_invalid_webhook_signature_is_rejected(self):
        payload = json.dumps({
            "event": "charge.success",
            "data": {
                "reference": self.donation.reference,
                "status": "success",
                "amount": 500000,
                "currency": "NGN"
            }
        })

        response = self.client.post(
            reverse("paystack_webhook"),
            data=payload,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE="invalid-signature"
        )

        self.donation.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.donation.status, "pending")

    @patch("AgricApp.views.send_donation_confirmation")
    @patch("AgricApp.views.send_admin_notification")
    def test_valid_webhook_marks_donation_paid(
        self, mock_admin_email, mock_donor_email
    ):
        payload = json.dumps({
            "event": "charge.success",
            "data": {
                "reference": self.donation.reference,
                "status": "success",
                "amount": 500000,
                "currency": "NGN"
            }
        })

        signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha512
        ).hexdigest()

        response = self.client.post(
            reverse("paystack_webhook"),
            data=payload,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE=signature
        )

        self.donation.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.donation.status, "paid")
        mock_donor_email.assert_called_once()
        mock_admin_email.assert_called_once()
