from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Company
from .forms import CompanyForm


def company_list(request):
    """
    Display a list of all registered companies with options to add, edit, and delete.
    Supports simple search by company name or job role.
    """
    search_query = request.GET.get('search', '').strip()
    if search_query:
        companies = Company.objects.filter(name__icontains=search_query) | Company.objects.filter(job_role__icontains=search_query)
    else:
        companies = Company.objects.all()

    context = {
        'companies': companies,
        'search_query': search_query,
    }
    return render(request, 'companies/company_list.html', context)


def company_create(request):
    """
    Handle adding a new company.
    """
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Company "{company.name}" has been successfully added!')
            return redirect('companies:company_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CompanyForm()

    context = {
        'form': form,
        'action_title': 'Add New Company',
        'button_text': 'Add Company',
    }
    return render(request, 'companies/company_form.html', context)


def company_update(request, pk):
    """
    Handle editing details of an existing company.
    """
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, f'Company "{company.name}" updated successfully!')
            return redirect('companies:company_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CompanyForm(instance=company)

    context = {
        'form': form,
        'company': company,
        'action_title': f'Edit Company: {company.name}',
        'button_text': 'Update Company',
    }
    return render(request, 'companies/company_form.html', context)


def company_delete(request, pk):
    """
    Handle deleting a company.
    Supports POST request directly (e.g. from popup confirm dialog) or fallback GET confirmation page.
    """
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        company_name = company.name
        company.delete()
        messages.success(request, f'Company "{company_name}" has been successfully deleted.')
        return redirect('companies:company_list')

    # Fallback confirmation view if accessed via direct GET
    return render(request, 'companies/company_confirm_delete.html', {'company': company})
