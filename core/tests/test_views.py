import shutil
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, SimpleTestCase
from django.urls import reverse
from ..models import Portfolio


INDEX_URL = reverse('index')
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class IndexViewTestCases(SimpleTestCase):
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
        self.assertTemplateUsed(response, 'core/home/index.html')

    def test_index_page_with_valid_data(self):
        """
        Testing home page with valid data on database
        Index view returns only status=True

        """
        for each in range(10):
            if each <= 4:
                # 5 status = True
                Portfolio.objects.create(**self.portfolio_data)
            else:
                # status = False
                Portfolio.objects.create(**self.portfolio_data, status=False)

        all_portfolio = Portfolio.objects.all()
        response = self.client.get(path=INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('portfolio'), 5)
        self.assertTrue(all_portfolio.count(), 10)
