import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ride.models import Ride


class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope["url_route"]["kwargs"]["ride_id"]
        self.group_name = f"ride_{self.ride_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        lat = data.get("lat")
        lon = data.get("lon")

        await self.update_ride_location(self.ride_id, lat, lon)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "location_update",
                "lat": lat,
                "lon": lon,
            },
        )

    async def location_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "2525252525",
                    "lat": event["lat"],
                    "lon": event["lon"],
                }
            )
        )

    @database_sync_to_async
    def update_ride_location(self, ride_id, lat, lon):
        ride = Ride.objects.get(id=ride_id)
        ride.current_location_lat = lat
        ride.current_location_lon = lon
        ride.save()
