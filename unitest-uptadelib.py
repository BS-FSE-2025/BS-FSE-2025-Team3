import unittest
from datetime import datetime, date
from django.test import Client, RequestFactory
from django.urls import reverse
from Base.views import update_library_hours
from Base.models import Library, LibraryHours

class TestUpdateLibraryHours(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.library = Library.objects.create(name="Test Library")

    def test_update_library_hours_post_valid_data(self):
        data = {
            "date": "2023-04-15",
            "opening_hours": "09:00",
            "closing_hours": "18:00",
            "library_id": self.library.id
        }
        request = self.factory.post(reverse("update_library_hours"), data=data)
        response = update_library_hours(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["message"], "Library hours updated successfully!")

        library_hours = LibraryHours.objects.get(library=self.library, date=date(2023, 4, 15))
        self.assertEqual(library_hours.opening_time, datetime.strptime("09:00", "%H:%M").time())
        self.assertEqual(library_hours.closing_time, datetime.strptime("18:00", "%H:%M").time())

    def test_update_library_hours_post_invalid_date(self):
        data = {
            "date": "2023-04-32",
            "opening_hours": "09:00",
            "closing_hours": "18:00",
            "library_id": self.library.id
        }
        request = self.factory.post(reverse("update_library_hours"), data=data)
        response = update_library_hours(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertIn("ValueError", response.json()["message"])

    def test_update_library_hours_post_invalid_time(self):
        data = {
            "date": "2023-04-15",
            "opening_hours": "25:00",
            "closing_hours": "18:00",
            "library_id": self.library.id
        }
        request = self.factory.post(reverse("update_library_hours"), data=data)
        response = update_library_hours(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertIn("ValueError", response.json()["message"])

    def test_update_library_hours_get_request(self):
        request = self.factory.get(reverse("update_library_hours"))
        response = update_library_hours(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "updatelibraryh.html")

if __name__ == "__main__":
    unittest.main()

