import shutil
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from ..models import Portfolio


INDEX_URL = reverse('index')
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class IndexViewTestCases(TestCase):
    databases = '__all__'

    def setUp(self):
        photo = SimpleUploadedFile(
            "test_photo.png",
            b"content_in_bytes",
            content_type='png'
        )
        photo_detail = SimpleUploadedFile(
            "test_photo.png",
            b"content_for_desc_in_bytes",
            content_type='png'
        )
        self.portfolio_data = {
            'title': 'testing_title',
            'description': 'description testing',
            'photo': photo,
            'photo_detail_page': photo_detail,
            'url': 'https://google.com',
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_index_page_without_any_data(self):
        """
        Testing home page without saving any data to database
        """
        response = self.client.get(path=INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')

    def test_index_page_with_valid_data(self):
        """
        Testing home page with valid data on database
        """
        for each in range(10):
            if each <= 5:
                Portfolio.objects.create(**self.portfolio_data)
            else:
                Portfolio.objects.create(**self.portfolio_data, status=False)

        query = Portfolio.objects.filter(status=True)

        response = self.client.get(path=INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context.get('portfolio'),
            query,
            transform=lambda x: x
        )
