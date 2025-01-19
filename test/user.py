from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class RiderViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a test rider
        self.rider = User.objects.create_user(
            email="test_rider@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="Rider",
            user_type=User.UserTypes.RIDER,
            username="test_rider@example.com",
        )
        # Endpoint URLs
        self.register_url = "/api/v1/auth/rider/register/"
        self.rider_url = "/api/v1/auth/rider/"
        # Authentication setup
        self.client.login(
            email="test_rider@example.com", password="testpassword123"
        )

    def test_rider_registration_success(self):
        payload = {
            "email": "new_rider@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "Rider",
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], payload["email"])

    def test_rider_registration_email_exists(self):
        payload = {
            "email": "test_rider@example.com",  # Email already exists
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "Rider",
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "User with this email already exists", str(response.data)
        )

    def test_get_rider_details_authenticated(self):
        self.client.force_authenticate(user=self.rider)
        response = self.client.get(self.rider_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.rider.email)

    def test_get_rider_details_unauthenticated(self):
        self.client.logout()  # Simulate unauthenticated access
        response = self.client.get(self.rider_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_rider_details(self):
        self.client.force_authenticate(user=self.rider)
        payload = {"first_name": "UpdatedName"}
        response = self.client.patch(self.rider_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "UpdatedName")

    def test_partial_update_rider_details_unauthenticated(self):
        self.client.logout()  # Simulate unauthenticated access
        payload = {"first_name": "UpdatedName"}
        response = self.client.patch(self.rider_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_rider_details_invalid_permission(self):
        # Create another user with a different user type
        another_user = User.objects.create_user(
            email="test_driver@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="Driver",
            user_type=User.UserTypes.DRIVER,
            username="test_driver@example.com",
        )
        self.client.force_authenticate(user=another_user)
        payload = {"first_name": "HackerName"}
        response = self.client.patch(self.rider_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DriverViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a test driver
        self.driver = User.objects.create_user(
            email="driver@gmail.com",
            password="driverpassword123",
            first_name="Test",
            last_name="Driver",
            user_type=User.UserTypes.DRIVER,
            username="driver@gmail.com",
            lat=0.0,
            long=0.0,
        )
        # Endpoint URLs
        self.register_url = "/api/v1/auth/driver/register/"
        self.driver_url = "/api/v1/auth/driver/"
        # Authentication setup
        self.client.login(
            email="driver@gmail.com", password="driverpassword123"
        )

    def test_driver_registration_success(self):
        payload = {
            "email": "new_driver@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "Driver",
            "lat": 0.0,
            "long": 0.0,
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], payload["email"])

    def test_driver_registration_email_exists(self):
        payload = {
            "email": "driver@gmail.com",  # Email already exists
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "Driver",
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "User with this email already exists", str(response.data)
        )

    def test_get_driver_details_authenticated(self):
        self.client.force_authenticate(user=self.driver)
        response = self.client.get(self.driver_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.driver.email)

    def test_get_driver_details_unauthenticated(self):
        self.client.logout()  # Simulate unauthenticated access
        response = self.client.get(self.driver_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_driver_details(self):
        self.client.force_authenticate(user=self.driver)
        payload = {"first_name": "UpdatedDriver"}
        response = self.client.patch(self.driver_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "UpdatedDriver")

    def test_partial_update_driver_details_unauthenticated(self):
        self.client.logout()  # Simulate unauthenticated access
        payload = {"first_name": "UpdatedDriver"}
        response = self.client.patch(self.driver_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_driver_details_invalid_permission(self):
        # Create another user with a different user type
        another_user = User.objects.create_user(
            email="another_user@example.com",
            password="anotherpassword123",
            first_name="Another",
            last_name="User",
            user_type=User.UserTypes.RIDER,
            username="another_user@example.com",
        )
        self.client.force_authenticate(user=another_user)
        payload = {"first_name": "HackerDriver"}
        response = self.client.patch(self.driver_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
