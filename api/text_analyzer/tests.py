from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from unittest.mock import patch
from .protocols.llm_protocol import ExtractedData


class TextAnalyzerAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("text_analyzer.serializers.LLMManager")
    def test_analyze_post(self, mock_llm_manager):
        mock_llm_manager.return_value.summarize.return_value = "Hello world"
        mock_llm_manager.return_value.get_metadata.return_value = ExtractedData(
            summarized_text="Hello world mocking",
            title="Greeting",
            topics=["Introduction"],
            sentiment="Positive",
            keywords=["hello", "world"],
        )

        url = reverse("textanalysis-list")
        data = {"text": "Hello world"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('"text":"Hello world"', response.content.decode())

    def test_search_get(self):
        url = reverse("textanalysis-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
