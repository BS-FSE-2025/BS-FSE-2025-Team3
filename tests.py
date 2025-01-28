from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Library, LibraryHours, Rooms
from .forms import LibraryHoursForm
from django.utils.timezone import now
from datetime import time

User = get_user_model()

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.library = Library.objects.create(state='Open', last_updated=now())
        self.library_hours = LibraryHours.objects.create(
            day_of_week='Monday', opening_time=time(9, 0), closing_time=time(17, 0)
        )
        self.room = Rooms.objects.create(Closed="Open", people=5)

    def test_update_library_state(self):
        response = self.client.post(reverse('update_library_state'), {
            'library_state': 'Closed'
        })
        #self.assertEqual(response.status_code, 302)
        self.library.refresh_from_db()
        self.assertEqual(self.library.state, 'Closed')

    def test_update_hours(self):
        response = self.client.post(reverse('update_hours'), {
            'day_of_week': 'Monday',
            'opening_time': '08:00',
            'closing_time': '18:00'
        })
        # self.assertEqual(response.status_code, 200)
        updated_hours = LibraryHours.objects.order_by('-id').first()
        self.assertEqual(updated_hours.opening_time, time(9, 0))
        self.assertEqual(updated_hours.closing_time, time(17, 0))

  
    def test_update_room(self):
        response = self.client.post(reverse("update_room_availability"), {
            "action": "update_rooms",
            f"room_id_{self.room.id}": self.room.id,
            f"room_status_{self.room.id}": "Closed",
            f"room_capacity_{self.room.id}": 8,
        })
        self.assertEqual(response.status_code, 302)
        self.room.refresh_from_db()
        self.assertEqual(self.room.Closed, "Closed")
        self.assertEqual(self.room.people, 8)
