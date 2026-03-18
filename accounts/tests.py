"""
Tests for authentication and user management.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from patients.models import Patient, Physiotherapist


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create patient user
        self.patient_user = User.objects.create_user(
            username="testpatient",
            password="testpass123",
            first_name="Test",
            last_name="Patient",
        )
        self.patient = Patient.objects.create(
            user=self.patient_user, age=30, condition="Test condition"
        )

        # Create physiotherapist user
        self.physio_user = User.objects.create_user(
            username="testphysio",
            password="testpass123",
            first_name="Test",
            last_name="Physio",
        )
        self.physio = Physiotherapist.objects.create(
            user=self.physio_user, license_number="TEST-123"
        )

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(
            "/accounts/login/", {"username": "testpatient", "password": "testpass123"}
        )
        self.assertRedirects(response, "/")

    def test_login_failure(self):
        """Test failed login with wrong password."""
        response = self.client.post(
            "/accounts/login/", {"username": "testpatient", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña incorrectos")

    def test_unauthenticated_access_redirects_to_login(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get("/")
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_authenticated_user_can_access(self):
        """Test that authenticated users can access the site."""
        self.client.login(username="testpatient", password="testpass123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test logout redirects to login."""
        self.client.login(username="testpatient", password="testpass123")
        response = self.client.get("/accounts/logout/")
        self.assertRedirects(response, "/accounts/login/")


class RoleTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create patient user
        self.patient_user = User.objects.create_user(
            username="testpatient", password="testpass123"
        )
        self.patient = Patient.objects.create(user=self.patient_user)

        # Create physiotherapist user
        self.physio_user = User.objects.create_user(
            username="testphysio", password="testpass123"
        )
        self.physio = Physiotherapist.objects.create(user=self.physio_user)

    def test_patient_sees_patient_badge(self):
        """Test that patient sees patient badge in navbar."""
        self.client.login(username="testpatient", password="testpass123")
        response = self.client.get("/")
        self.assertContains(response, "Pac")

    def test_physio_sees_physio_badge(self):
        """Test that physiotherapist sees physiotherapist badge."""
        self.client.login(username="testphysio", password="testpass123")
        response = self.client.get("/")
        self.assertContains(response, "PT")

    def test_physio_can_access_patients_list(self):
        """Test that physiotherapist can access patients list."""
        self.client.login(username="testphysio", password="testpass123")
        response = self.client.get("/accounts/pacientes/")
        self.assertEqual(response.status_code, 200)

    def test_patient_cannot_access_patients_list(self):
        """Test that patient cannot access patients list."""
        self.client.login(username="testpatient", password="testpass123")
        response = self.client.get("/accounts/pacientes/")
        self.assertEqual(response.status_code, 302)  # Redirect


class ImpersonationTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create patient user
        self.patient_user = User.objects.create_user(
            username="testpatient",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )
        self.patient = Patient.objects.create(user=self.patient_user)

        # Create physiotherapist user
        self.physio_user = User.objects.create_user(
            username="testphysio", password="testpass123"
        )
        self.physio = Physiotherapist.objects.create(user=self.physio_user)

    def test_physio_can_impersonate_patient(self):
        """Test that physiotherapist can impersonate a patient."""
        self.client.login(username="testphysio", password="testpass123")
        response = self.client.get(f"/accounts/impersonate/{self.patient_user.id}/")
        self.assertEqual(response.status_code, 302)

        # Check session has impersonation
        session = self.client.session
        self.assertEqual(session.get("impersonating_user_id"), self.patient_user.id)

    def test_impersonation_shows_in_navbar(self):
        """Test that impersonation is shown in navbar."""
        self.client.login(username="testphysio", password="testpass123")

        # Impersonate patient
        self.client.get(f"/accounts/impersonate/{self.patient_user.id}/")

        response = self.client.get("/")
        self.assertContains(response, "Ver como")
        self.assertContains(response, "John Doe")

    def test_stop_impersonation(self):
        """Test stopping impersonation."""
        self.client.login(username="testphysio", password="testpass123")

        # Impersonate patient
        self.client.get(f"/accounts/impersonate/{self.patient_user.id}/")

        # Stop impersonation
        response = self.client.get("/accounts/stop-impersonate/")
        self.assertEqual(response.status_code, 302)

        # Check session is cleared
        session = self.client.session
        self.assertIsNone(session.get("impersonating_user_id"))

    def test_patient_cannot_impersonate(self):
        """Test that patient cannot impersonate other patients."""
        # Create another patient
        other_patient_user = User.objects.create_user(
            username="otherpatient", password="testpass123"
        )
        Patient.objects.create(user=other_patient_user)

        self.client.login(username="testpatient", password="testpass123")
        response = self.client.get(f"/accounts/impersonate/{other_patient_user.id}/")
        self.assertEqual(response.status_code, 302)  # Redirect


class PasswordChangeTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="testuser", password="oldpass123")
        Patient.objects.create(user=self.user)

    def test_password_change(self):
        """Test password change functionality."""
        self.client.login(username="testuser", password="oldpass123")

        response = self.client.post(
            "/accounts/password/",
            {
                "old_password": "oldpass123",
                "new_password1": "newpass123",
                "new_password2": "newpass123",
            },
        )

        # Check redirect to done page
        self.assertRedirects(response, "/accounts/password/done/")

        # Check new password works
        self.assertTrue(self.client.login(username="testuser", password="newpass123"))
