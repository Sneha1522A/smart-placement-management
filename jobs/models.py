from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Internship', 'Internship'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=150, verbose_name="Job Title")
    company = models.CharField(max_length=150, verbose_name="Company Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, verbose_name="Job Type")
    package = models.CharField(max_length=50, blank=True, null=True, verbose_name="Package / CTC (e.g. 12 LPA)")
    description = models.TextField(verbose_name="Job Description")
    min_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name="Minimum CGPA"
    )
    eligible_branches = models.CharField(
        max_length=200,
        help_text="Comma-separated branches (e.g., CSE, ECE, ISE, ME)",
        verbose_name="Eligible Branches"
    )
    deadline = models.DateField(verbose_name="Application Deadline")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Posted At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"

    def __str__(self):
        return f"{self.title} at {self.company}"
