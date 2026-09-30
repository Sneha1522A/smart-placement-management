/**
 * Smart Placement Management System (SPMS) - Company Management JavaScript
 * Handles delete confirmation popup modal and interactive UI enhancements.
 */

document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------
    // Delete Confirmation Popup Modal Handler
    // -------------------------------------------------------------
    const deleteModal = document.getElementById('deleteConfirmModal');
    const deleteModalForm = document.getElementById('deleteModalForm');
    const deleteCompanyNameSpan = document.getElementById('deleteCompanyName');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');

    // Attach click event to all delete trigger buttons
    const deleteButtons = document.querySelectorAll('.btn-delete-trigger');
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const companyId = this.getAttribute('data-company-id');
            const companyName = this.getAttribute('data-company-name');
            const deleteUrl = this.getAttribute('data-delete-url');

            if (deleteModal && deleteModalForm) {
                // Show modal popup
                deleteModalForm.setAttribute('action', deleteUrl);
                if (deleteCompanyNameSpan) {
                    deleteCompanyNameSpan.textContent = companyName;
                }
                deleteModal.classList.add('active');
            } else {
                // Fallback to standard browser confirmation dialog if modal is unavailable
                const confirmed = window.confirm(`Are you sure you want to delete "${companyName}"? This action cannot be undone.`);
                if (confirmed) {
                    // Create and submit a POST form with CSRF token
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = deleteUrl;

                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
                    if (csrfToken) {
                        const csrfInput = document.createElement('input');
                        csrfInput.type = 'hidden';
                        csrfInput.name = 'csrfmiddlewaretoken';
                        csrfInput.value = csrfToken;
                        form.appendChild(csrfInput);
                    }
                    document.body.appendChild(form);
                    form.submit();
                }
            }
        });
    });

    // Close modal when "Cancel" button is clicked
    if (cancelDeleteBtn && deleteModal) {
        cancelDeleteBtn.addEventListener('click', function () {
            deleteModal.classList.remove('active');
        });
    }

    // Close modal when clicking outside the dialog card
    if (deleteModal) {
        deleteModal.addEventListener('click', function (e) {
            if (e.target === deleteModal) {
                deleteModal.classList.remove('active');
            }
        });

        // Close on Escape key press
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && deleteModal.classList.contains('active')) {
                deleteModal.classList.remove('active');
            }
        });
    }

    // -------------------------------------------------------------
    // Alert Auto-Dismiss
    // -------------------------------------------------------------
    const alertDismissButtons = document.querySelectorAll('.alert-dismiss');
    alertDismissButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                alert.style.transition = 'all 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }
        });
    });

    // Automatically fade out alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (alert && alert.parentElement) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                alert.style.transition = 'all 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    });
});
