from django.test import TestCase
from ..homepage.models import Service, Intervention, Doctor_TMP

class ServiceModelTestCase(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Test Service',
            slug='test-service',
            description='This is a test service',
            image='test_image.jpg'
        )

    def test_service_name(self):
        self.assertEqual(self.service.name, 'Test Service')

    def test_service_slug(self):
        self.assertEqual(self.service.slug, 'test-service')

    def test_service_description(self):
        self.assertEqual(self.service.description, 'This is a test service')

    def test_service_image(self):
        self.assertEqual(self.service.image, 'test_image.jpg')


class InterventionModelTestCase(TestCase):
    def setUp(self):
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

    def test_intervention_name(self):
        self.assertEqual(self.intervention.name, 'Test Intervention')

    def test_intervention_description(self):
        self.assertEqual(self.intervention.description, 'This is a test intervention')

    def test_intervention_service(self):
        self.assertEqual(self.intervention.service, self.service)


class Doctor_TMPModelTestCase(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Test Service',
            slug='test-service',
            description='This is a test service',
            image='test_image.jpg'
        )
        self.doctor = Doctor_TMP.objects.create(
            fullname='Test Doctor',
            qualification='Test Qualification',
            service=self.service
        )

    def test_doctor_fullname(self):
        self.assertEqual(self.doctor.fullname, 'Test Doctor')

    def test_doctor_qualification(self):
        self.assertEqual(self.doctor.qualification, 'Test Qualification')

    def test_doctor_service(self):
        self.assertEqual(self.doctor.service, self.service)