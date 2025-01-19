from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ride.models import Ride

User = get_user_model()


class RideViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a rider user
        self.rider = User.objects.create_user(
            email="rider@example.com",
            password="riderpassword123",
            first_name="Rider",
            last_name="User",
            user_type=User.UserTypes.RIDER,
            username="rider@example.com",
        )


        # Create a ride
        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="Pickup Location A",
            pickup_location_lat=12.971598,
            pickup_location_lon=77.594566,
            dropoff_location="Dropoff Location B",
            status=Ride.RideStatus.REQUESTED,
        )

        # API endpoints
        self.rides_url = "/api/v1/rider/rides/"
        self.update_status_url = f"/api/v1/rider/ride/{self.ride.id}/"

    def authenticate_rider(self):
        """Authenticate the rider user."""
        self.client.force_authenticate(user=self.rider)

    def test_list_rides(self):
        """Test listing all rides for the authenticated rider."""
        self.authenticate_rider()
        response = self.client.get(self.rides_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(
            response.data["results"][0]["pickup_location"],
            self.ride.pickup_location,
        )

    def test_create_ride_success(self):
        """Test creating a ride successfully."""
        payload = {
            "pickup_location": "Pickup Location C",
            "pickup_location_lat": 13.0001,
            "pickup_location_lon": 77.6001,
            "dropoff_location": "Dropoff Location D",
        }
        self.authenticate_rider()
        response = self.client.post(self.rides_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["pickup_location"], payload["pickup_location"]
        )
        self.assertEqual(
            response.data["dropoff_location"], payload["dropoff_location"]
        )

    def test_create_ride_unauthenticated(self):
        """Test creating a ride without authentication."""
        
        payload = {
            "pickup_location": "Pickup Location C",
            "pickup_location_lat": 13.0001,
            "pickup_location_lon": 77.6001,
            "dropoff_location": "Dropoff Location D",
        }
        response = self.client.post(self.rides_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_ride_status_success(self):
        """Test updating the status of a ride successfully."""
        self.authenticate_rider()
        payload = {"status": "IN_PROGRESS"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, "IN_PROGRESS")

    def test_update_ride_status_invalid(self):
        """Test updating the ride status with an invalid value."""
        self.authenticate_rider()
        payload = {"status": "INVALID_STATUS"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ride_status_unauthenticated(self):
        """Test updating the ride status without authentication."""
        self.client.logout()
        payload = {"status": "IN_PROGRESS"}
        response = self.client.patch(self.update_status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_rides_unauthenticated(self):
        """Test listing rides without authentication."""
        self.client.logout()
        response = self.client.get(self.rides_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
