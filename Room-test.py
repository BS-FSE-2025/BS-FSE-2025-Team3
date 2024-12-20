from django.test import TestCase
from django.urls import reverse
from .models import Room  # Make sure to import the Room model

class RoomListViewTests(TestCase):

    def setUp(self):
        # Create some test rooms
        Room.objects.create(name="Room A")
        Room.objects.create(name="Room B")

    def test_room_list_view_status_code(self):
        response = self.client.get(reverse('room_list'))  # Replace 'room_list' with the actual name of your URL pattern
        self.assertEqual(response.status_code, 200)

    def test_room_list_view_template_used(self):
        response = self.client.get(reverse('room_list'))
        self.assertTemplateUsed(response, 'rooms/room_list.html')

    def test_room_list_view_context(self):
        response = self.client.get(reverse('room_list'))
        self.assertIn('rooms', response.context)
        self.assertEqual(len(response.context['rooms']), 2)  # Check if we have 2 rooms in context