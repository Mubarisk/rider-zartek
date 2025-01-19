from django.test import TestCase
from ride.models import Ride
from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import ACos, Cos, Radians, Sin

User = get_user_model()


# 10.846168515698126, 75.95346250449533
# 10.846924639561188, 75.95351382969358
# 10.847346235073221, 75.95304257105485
# 10.848473541890229, 75.95310322810732
class RideMatchingTestCase(TestCase):
    def setUp(self):
        # Create a driver with a specific location
        self.driver = User.objects.create_user(
            email="driver@example.com",
            password="driverpassword123",
            first_name="Driver",
            last_name="User",
            user_type=User.UserTypes.DRIVER,
            username="driver@example.com",
            lat=10.846168515698126,  # Driver's latitude
            long=75.95346250449533,  # Driver's longitude
        )
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
        # Create rides with varying pickup locations
        self.ride1 = Ride.objects.create(
            rider=self.rider,
            pickup_location="Pickup Location 1",
            pickup_location_lat=10.846924639561188,
            pickup_location_lon=75.95351382969358,
            dropoff_location="Dropoff Location 1",
            status=Ride.RideStatus.REQUESTED,
        )

        self.ride2 = Ride.objects.create(
            rider=self.rider,
            pickup_location="Pickup Location 2",
            pickup_location_lat=10.848473541890229,
            pickup_location_lon=75.95310322810732,
            dropoff_location="Dropoff Location 2",
            status=Ride.RideStatus.REQUESTED,
        )

        self.ride3 = Ride.objects.create(
            rider=self.rider,
            pickup_location="Pickup Location 3",
            pickup_location_lat=10.847346235073221,
            pickup_location_lon=75.95304257105485,
            dropoff_location="Dropoff Location 3",
            status=Ride.RideStatus.REQUESTED,
        )

    def test_proximity_ordering(self):
        """Test that rides are ordered by proximity to the driver's location."""
        # Simulate the ride matching algorithm
        user_lat = self.driver.lat
        user_lon = self.driver.long

        rides = Ride.objects.annotate(
            distance=ExpressionWrapper(
                6371
                * ACos(
                    Cos(Radians(user_lat))
                    * Cos(Radians(F("pickup_location_lat")))
                    * Cos(
                        Radians(F("pickup_location_lon")) - Radians(user_lon)
                    )
                    + Sin(Radians(user_lat))
                    * Sin(Radians(F("pickup_location_lat")))
                ),
                output_field=FloatField(),
            )
        ).order_by("distance")

        # Get ride IDs in the calculated order
        ride_ids = list(rides.values_list("id", flat=True))
        # print(ride_ids,'----------------')
        # Manually verify the expected order
        self.assertEqual(
            ride_ids, [self.ride1.id, self.ride3.id, self.ride2.id]
        )

    def test_no_driver_location(self):
        """Test ride listing when the driver's location is not set."""
        self.driver.lat = 0.0
        self.driver.long = 0.0
        self.driver.save()

        rides = Ride.objects.all().order_by("-created_at")

        self.assertEqual(len(rides), 3)
        self.assertIn(self.ride1, rides)
        self.assertIn(self.ride2, rides)
        self.assertIn(self.ride3, rides)

    def test_no_rides_available(self):
        """Test ride listing when no rides are available."""
        Ride.objects.all().delete()  # Remove all rides
        rides = Ride.objects.all()
        self.assertEqual(len(rides), 0)

    def test_same_location_rides(self):
        """Test behavior when multiple rides have the same pickup location."""
        Ride.objects.create(
            rider=self.rider,
            pickup_location="Duplicate Location",
            pickup_location_lat=12.971891,
            pickup_location_lon=77.641151,
            dropoff_location="Dropoff Location Duplicate",
            status=Ride.RideStatus.REQUESTED,
        )

        rides = Ride.objects.annotate(
            distance=ExpressionWrapper(
                6371
                * ACos(
                    Cos(Radians(self.driver.lat))
                    * Cos(Radians(F("pickup_location_lat")))
                    * Cos(
                        Radians(F("pickup_location_lon"))
                        - Radians(self.driver.long)
                    )
                    + Sin(Radians(self.driver.lat))
                    * Sin(Radians(F("pickup_location_lat")))
                ),
                output_field=FloatField(),
            )
        ).order_by("distance")

        # Ensure all rides at the same location are included
        self.assertEqual(len(rides), 4)
