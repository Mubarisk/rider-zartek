from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ride.models import Ride

User = get_user_model()


class DriverRideViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a driver user
        self.driver = User.objects.create_user(
            email="driver@example.com",
            password="driverpassword123",
            first_name="Driver",
            last_name="User",
            user_type=User.UserTypes.DRIVER,
            username="driver@example.com",
            lat=12.971598,
            long=77.594566,
        )

        # Create a rider user
        self.rider = User.objects.create_user(
            email="rider@example.com",
            password="riderpassword123",
            first_name="Rider",
            last_name="User",
            user_type=User.UserTypes.RIDER,
            username="rider@example.com",
            lat=0.0,
            long=0.0,
        )

        # Create a ride requested by the rider
        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="Pickup Point A",
            pickup_location_lat=12.971891,
            pickup_location_lon=77.641151,
            dropoff_location="Dropoff Point B",
            status=Ride.RideStatus.REQUESTED,  # Ensure status matches queryset
            driver=None,
        )

        # API endpoints
        self.rides_url = "/api/v1/driver/rides/"
        self.update_status_url = f"/api/v1/driver/ride/{self.ride.id}/"
        self.my_rides_url = "/api/v1/driver/my-rides/"

    def authenticate_driver(self):
        """Authenticate the driver user."""
        self.client.force_authenticate(user=self.driver)

    def test_list_rides(self):
        """Test listing all available rides."""
        self.authenticate_driver()
        response = self.client.get(self.rides_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["pickup_location"],
            self.ride.pickup_location,
        )

    def test_update_ride_status_to_accepted(self):
        """Test updating ride status to 'ACCEPTED'."""
        self.authenticate_driver()
        payload = {"status": "ACCEPTED"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, "ACCEPTED")
        self.assertEqual(self.ride.driver, self.driver)

    def test_update_ride_status_to_completed(self):
        """Test updating ride status to 'COMPLETED'."""
        self.ride.driver = self.driver
        self.ride.status = Ride.RideStatus.ACCEPTED
        self.ride.save()

        self.authenticate_driver()
        payload = {"status": "COMPLETED"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, "COMPLETED")

    def test_update_ride_status_unauthorized_driver(self):
        """Test updating ride status with an unauthorized driver."""
        self.ride.driver = self.rider  # Assign a different driver
        self.ride.save()

        self.authenticate_driver()
        payload = {"status": "IN_PROGRESS"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_invalid_ride_status(self):
        """Test updating ride status to an invalid value."""
        self.authenticate_driver()
        payload = {"status": "INVALID_STATUS"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_my_rides(self):
        """Test listing the authenticated driver's rides."""
        self.ride.driver = self.driver
        self.ride.status = Ride.RideStatus.IN_PROGRESS
        self.ride.save()

        self.authenticate_driver()
        response = self.client.get(self.my_rides_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["pickup_location"],
            self.ride.pickup_location,
        )

    def test_list_my_rides_no_rides(self):
        """Test listing my rides when no rides are assigned."""
        self.authenticate_driver()
        response = self.client.get(self.my_rides_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 0)

    def test_list_rides_unauthenticated(self):
        """Test listing rides without authentication."""
        response = self.client.get(self.rides_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_ride_status_unauthenticated(self):
        """Test updating ride status without authentication."""
        payload = {"status": "COMPLETED"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
