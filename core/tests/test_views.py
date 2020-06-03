import shutil
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, SimpleTestCase
from django.urls import reverse
from ..models import Portfolio
from ..forms import ContactMessageForm

MEDIA_ROOT = tempfile.mkdtemp()


def create_portfolio(**data):
    return Portfolio.objects.create(**data)


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
        self.index_url = reverse('index')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_index_page_without_any_data(self):
        """
        Testing home page without saving any data to database
        """
        response = self.client.get(path=self.index_url)
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
                create_portfolio(**self.portfolio_data)
            else:
                # status = False
                create_portfolio(**self.portfolio_data, status=False)

        all_portfolio = Portfolio.objects.all()
        response = self.client.get(path=self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('portfolio'), 5)
        self.assertTrue(all_portfolio.count(), 10)


class ContactViewTestCases(SimpleTestCase):
    databases = '__all__'

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/index.html')
        self.assertIsInstance(response.context.get('form'), ContactMessageForm)


class PortfolioDetailViewTestCases(SimpleTestCase):
    databases = '__all__'

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
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

    def test_portfolioO(self):
        portfolio = create_portfolio(**self.portfolio_data)
        url = reverse('portfolio', kwargs={'pk': portfolio.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio-details.html')
