from django.test import TestCase, Client
from django.urls import reverse
from your_app.models import library  # Replace 'your_app' with your actual app name

class LibraryViewTests(TestCase):
    def setUp(self):
        """Set up test data before each test method"""
        self.client = Client()
        
        # Create some test library objects
        self.library1 = library.objects.create(
            # Add required fields for your library model
            name="Library 1"
            # Add other fields as needed
        )
        self.library2 = library.objects.create(
            name="Library 2"
            # Add other fields as needed
        )

    def test_available_library_view_status(self):
        """Test that view returns correct status code"""
        response = self.client.get(reverse('available-library'))
        self.assertEqual(response.status_code, 200)

    def test_available_library_template(self):
        """Test that correct template is used"""
        response = self.client.get(reverse('available-library'))
        self.assertTemplateUsed(response, 'AvailableLibrary.html')

    def test_available_library_context(self):
        """Test that context contains all libraries"""
        response = self.client.get(reverse('available-library'))
        
        # Check that 'libraries' exists in context
        self.assertIn('libraries', response.context)
        
        # Get the libraries from context
        context_libraries = response.context['libraries']
        
        # Check that all libraries are present
        self.assertEqual(len(context_libraries), 2)
        
        # Check that our test libraries are in the queryset
        self.assertIn(self.library1, context_libraries)
        self.assertIn(self.library2, context_libraries)

    def test_available_library_empty_database(self):
        """Test view behavior when no libraries exist"""
        # Delete all libraries
        library.objects.all().delete()
        
        response = self.client.get(reverse('available-library'))
        
        # Check that the view still works
        self.assertEqual(response.status_code, 200)
        
        # Check that context contains empty queryset
        self.assertEqual(len(response.context['libraries']), 0)

    def test_available_library_queryset_ordering(self):
        """Test that libraries are retrieved in expected order"""
        response = self.client.get(reverse('available-library'))
        context_libraries = response.context['libraries']
        
        # Verify the queryset matches what we expect from objects.all()
        expected_libraries = library.objects.all()
        self.assertQuerysetEqual(
            context_libraries,
            expected_libraries,
            transform=lambda x: x
        )
