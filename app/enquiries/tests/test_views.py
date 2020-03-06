from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from app.enquiries.tests.factories import EnquiryFactory


class EnquiryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_enquiry_list(self):
        enquiries =  [EnquiryFactory() for i in range(5)]
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = response.data['serializer']['results']
        self.assertEqual(len(serializer), len(enquiries))

    def test_enquiries_list_pagination(self):
        """
        Tests pagination of enquiries list view.
        Creates enquiries and retrieves single page of results each time
        and ensures we get the expected number of results for that page.
        It will be same for all pages except for the last page
        if num_enquiries is not a multiple of page_size
        """
        num_enquiries = 54
        enquiries =  [EnquiryFactory() for i in range(num_enquiries)]
        page_size = settings.ENQUIRIES_PER_PAGE
        total_pages = (num_enquiries // page_size) + 1
        expected_counts = {}
        for i in range(1, total_pages + 1):
            if num_enquiries > page_size:
                expected_counts[i] = page_size
                num_enquiries -= page_size
            else:
                expected_counts[i] = num_enquiries % page_size

        for page, num_results in expected_counts.items():
            response = self.client.get(reverse("enquiry-list"), {"page": page})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            serializer = response.data['serializer']['results']
            self.assertEqual(len(serializer), num_results)
