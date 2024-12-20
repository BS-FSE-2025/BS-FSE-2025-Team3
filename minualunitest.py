from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from Base.models import Library, LibraryHours

class UpdateLibraryHoursTest(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a sample library for testing
        self.library = Library.objects.create(name="Test Library", address="123 Test St")

        # URL for the update library hours view
        self.url = reverse('update_library_hours')

    def test_get_request_renders_form(self):
        """Test that a GET request renders the HTML form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'updatelibraryh.html')

    def test_post_request_creates_library_hours(self):
        """Test that a POST request creates or updates library hours."""
        post_data = {
            "date": "2024-12-25",
            "opening_hours": "09:00",
            "closing_hours": "18:00",
            "library_id": self.library.id,
        }
        response = self.client.post(self.url, data=post_data, content_type="application/x-www-form-urlencoded")

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True, "message": "Library hours updated successfully!"})

        # Verify database entry
        library_hours = LibraryHours.objects.get(library=self.library, date="2024-12-25")
        self.assertEqual(library_hours.opening_time, datetime.strptime("09:00", "%H:%M").time())
        self.assertEqual(library_hours.closing_time, datetime.strptime("18:00", "%H:%M").time())

    def test_post_request_invalid_data(self):
        """Test that a POST request with invalid data returns an error."""
        post_data = {
            "date": "invalid-date",
            "opening_hours": "invalid-time",
            "closing_hours": "invalid-time",
            "library_id": self.library.id,
        }
        response = self.client.post(self.url, data=post_data, content_type="application/x-www-form-urlencoded")

        # Check response
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertFalse(response_json["success"])
        self.assertIn("time data", response_json["message"])  # Check for validation error in message

    def test_post_request_missing_library(self):
        """Test that a POST request fails if the library does not exist."""
        post_data = {
            "date": "2024-12-25",
            "opening_hours": "09:00",
            "closing_hours": "18:00",
            "library_id": 999,  # Non-existent library ID
        }
        response = self.client.post(self.url, data=post_data, content_type="application/x-www-form-urlencoded")

        # Check response
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertFalse(response_json["success"])
        self.assertIn("matching query does not exist", response_json["message"])  # Library not found error
