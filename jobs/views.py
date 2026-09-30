from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Job
from .forms import JobForm


@login_required
def job_management(request):
    """
    View for placement admins to view and post jobs.
    Restricted to logged-in staff users.
    """
    if not request.user.is_staff:
        raise PermissionDenied("Access restricted to placement staff admins only.")

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, f"Job posting '{job.title}' at {job.company} was successfully created!")
            return redirect('jobs:job_management')
        else:
            messages.error(request, "Failed to create job posting. Please correct the errors highlighted below.")
    else:
        form = JobForm()

    jobs = Job.objects.all()
    context = {
        'form': form,
        'jobs': jobs,
        'page_title': 'Job management',
    }
    return render(request, 'jobs/job_management.html', context)
