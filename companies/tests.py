from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import Company


class CompanyModelAndViewsTest(TestCase):
    """
    Test suite for the Company model and CRUD views.
    """

    def setUp(self):
        self.company = Company.objects.create(
            name="Google",
            job_role="Software Engineer",
            package_lpa=25.00,
            min_cgpa=8.00,
            deadline=date(2026, 10, 15)
        )

    def test_company_creation_and_str(self):
        """Test model creation and string representation."""
        self.assertEqual(str(self.company), "Google - Software Engineer (25.00 LPA)")
        self.assertEqual(self.company.name, "Google")
        self.assertEqual(self.company.job_role, "Software Engineer")
        self.assertEqual(self.company.package_lpa, 25.00)
        self.assertEqual(self.company.min_cgpa, 8.00)

    def test_company_list_view(self):
        """Test listing companies."""
        response = self.client.get(reverse('companies:company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google")
        self.assertContains(response, "Software Engineer")

    def test_company_create_view(self):
        """Test creating a company via form submission."""
        response = self.client.post(reverse('companies:company_create'), {
            'name': 'Microsoft',
            'job_role': 'Cloud Solutions Architect',
            'package_lpa': '22.50',
            'min_cgpa': '7.50',
            'deadline': '2026-11-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Company.objects.filter(name='Microsoft').exists())

    def test_company_update_view(self):
        """Test updating an existing company."""
        response = self.client.post(reverse('companies:company_update', args=[self.company.pk]), {
            'name': 'Google LLC',
            'job_role': 'Senior Software Engineer',
            'package_lpa': '32.00',
            'min_cgpa': '8.50',
            'deadline': '2026-10-20',
        })
        self.assertEqual(response.status_code, 302)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'Google LLC')
        self.assertEqual(self.company.job_role, 'Senior Software Engineer')

    def test_company_delete_view(self):
        """Test deleting a company."""
        response = self.client.post(reverse('companies:company_delete', args=[self.company.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Company.objects.filter(pk=self.company.pk).exists())
