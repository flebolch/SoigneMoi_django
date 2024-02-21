from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import Http404
from ..homepage.models import Service, Intervention, Doctor_TMP
from ..homepage.views import service

class ServiceViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.service = Service.objects.create(
            name='Test Service',
            slug='test-service',
            description='This is a test service',
            image='test_image.jpg'
        )
        self.intervention = Intervention.objects.create(
            name='Test Intervention',
            description='This is a test intervention',
            service=self.service
        )
        self.doctor = Doctor_TMP.objects.create(
            fullname='Test Doctor',
            qualification='Test Qualification',
            service=self.service
        )

    def test_service_view_with_valid_slug(self):
        url = reverse('service', kwargs={'Service_slug': 'test-service'})
        request = self.factory.get(url)
        response = service(request, Service_slug='test-service')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['services'], self.service)
        self.assertEqual(list(response.context['interventions']), [self.intervention])
        self.assertEqual(list(response.context['doctors']), [self.doctor])
        self.assertEqual(response.context['service_image'], 'test_image.jpg')

    def test_service_view_with_invalid_slug(self):
        url = reverse('service', kwargs={'Service_slug': 'invalid-slug'})
        request = self.factory.get(url)
        with self.assertRaises(Http404):
            service(request, Service_slug='invalid-slug')