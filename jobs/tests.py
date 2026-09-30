from datetime import date, timedelta
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Job
from .forms import JobForm


class JobModelTest(TestCase):
    def test_create_job(self):
        job = Job.objects.create(
            title="Software Engineer",
            company="Google",
            location="Bengaluru",
            job_type="Full-time",
            package="30 LPA",
            description="Build scalable distributed backend microservices.",
            min_cgpa=Decimal("8.50"),
            eligible_branches="CSE, ECE, ISE",
            deadline=date.today() + timedelta(days=30),
            status="Open"
        )
        self.assertEqual(str(job), "Software Engineer at Google")
        self.assertEqual(job.status, "Open")
        self.assertEqual(job.min_cgpa, Decimal("8.50"))

    def test_job_ordering(self):
        job1 = Job.objects.create(
            title="Job 1", company="Company A", location="Loc A",
            job_type="Full-time", description="Desc 1", min_cgpa=Decimal("7.0"),
            eligible_branches="CSE", deadline=date.today() + timedelta(days=10)
        )
        job2 = Job.objects.create(
            title="Job 2", company="Company B", location="Loc B",
            job_type="Internship", description="Desc 2", min_cgpa=Decimal("6.5"),
            eligible_branches="ECE", deadline=date.today() + timedelta(days=15)
        )
        jobs = list(Job.objects.all())
        self.assertEqual(jobs, [job2, job1])


class JobFormTest(TestCase):
    def test_valid_job_form(self):
        form_data = {
            'title': 'Frontend Engineer',
            'company': 'Microsoft',
            'location': 'Hyderabad',
            'job_type': 'Full-time',
            'package': '24 LPA',
            'description': 'Develop React and TypeScript web UI.',
            'min_cgpa': '7.50',
            'eligible_branches': 'CSE, ISE',
            'deadline': (date.today() + timedelta(days=20)).strftime('%Y-%m-%d'),
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_past_deadline_validation(self):
        past_date = date.today() - timedelta(days=5)
        form_data = {
            'title': 'Data Analyst',
            'company': 'Amazon',
            'location': 'Bengaluru',
            'job_type': 'Internship',
            'description': 'Analyze large datasets using SQL and Python.',
            'min_cgpa': '7.00',
            'eligible_branches': 'CSE, ISE',
            'deadline': past_date.strftime('%Y-%m-%d'),
        }
        form = JobForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('deadline', form.errors)
        self.assertEqual(form.errors['deadline'], ['Deadline cannot be in the past.'])

    def test_invalid_cgpa_validation(self):
        form_data = {
            'title': 'DevOps Engineer',
            'company': 'Meta',
            'location': 'Remote',
            'job_type': 'Full-time',
            'description': 'Manage Kubernetes clusters and CI/CD pipelines.',
            'min_cgpa': '11.50',
            'eligible_branches': 'CSE',
            'deadline': (date.today() + timedelta(days=10)).strftime('%Y-%m-%d'),
        }
        form = JobForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('min_cgpa', form.errors)
        self.assertEqual(form.errors['min_cgpa'], ['Minimum CGPA must be between 0.00 and 10.00.'])


class JobManagementViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='admin_user', password='password123', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='student_user', password='password123', is_staff=False
        )
        self.url = reverse('jobs:job_management')

    def test_unauthenticated_user_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_non_staff_user_denied(self):
        self.client.login(username='student_user', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_staff_user_get_job_management(self):
        self.client.login(username='admin_user', password='password123')
        Job.objects.create(
            title="Backend Developer", company="Oracle", location="Bengaluru",
            job_type="Full-time", description="Java & Spring Boot dev",
            min_cgpa=Decimal("7.0"), eligible_branches="CSE",
            deadline=date.today() + timedelta(days=14)
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_management.html')
        self.assertContains(response, "Job management")
        self.assertContains(response, "Backend Developer")

    def test_staff_user_post_create_job(self):
        self.client.login(username='admin_user', password='password123')
        valid_data = {
            'title': 'AI/ML Engineer',
            'company': 'NVIDIA',
            'location': 'Pune',
            'job_type': 'Full-time',
            'package': '28 LPA',
            'description': 'Train deep learning models for computer vision.',
            'min_cgpa': '8.50',
            'eligible_branches': 'CSE, AI/ML',
            'deadline': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
        }
        response = self.client.post(self.url, data=valid_data)
        self.assertRedirects(response, self.url)
        self.assertTrue(Job.objects.filter(title='AI/ML Engineer', company='NVIDIA').exists())
