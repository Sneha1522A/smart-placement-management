from django.db import models


class Company(models.Model):
    """
    Model representing a recruiting company in the placement portal.
    Stores company information, offered job role, package, CGPA criteria, and deadline.
    """
    name = models.CharField(max_length=200, verbose_name="Company Name")
    job_role = models.CharField(max_length=200, verbose_name="Job Role")
    package_lpa = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        verbose_name="Package (LPA)", 
        help_text="Annual salary package in Lakhs Per Annum (e.g. 12.50)"
    )
    min_cgpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        verbose_name="Minimum CGPA", 
        help_text="Minimum CGPA required to apply (e.g. 7.50)"
    )
    deadline = models.DateField(
        verbose_name="Application Deadline",
        help_text="Last date to apply for this company"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['deadline', 'name']

    def __str__(self):
        return f"{self.name} - {self.job_role} ({self.package_lpa:.2f} LPA)"

