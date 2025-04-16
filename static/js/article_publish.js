// Add this to a JavaScript file or include it in your template
document.addEventListener('DOMContentLoaded', function() {
    // Handle publish toggle buttons
    const publishButtons = document.querySelectorAll('.publish-toggle');

    publishButtons.forEach(button => {
        button.addEventListener('click', function() {
            const articleId = this.getAttribute('data-article-id');

            // Send AJAX request
            fetch(`/articles/${articleId}/toggle-publish/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update button appearance
                    if (data.is_published) {
                        this.classList.remove('btn-outline-success');
                        this.classList.add('btn-success');
                        this.innerHTML = '<i class="fas fa-check-circle"></i> Published';
                        this.title = 'Published';
                    } else {
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-success');
                        this.innerHTML = '<i class="far fa-circle"></i> Publish';
                        this.title = 'Unpublished';
                    }

                    // Show a toast or notification
                    showToast(data.message);
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred while updating publish status', 'error');
            });
        });
    });

    // Helper function for CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Simple toast notification function
    function showToast(message, type = 'success') {
        const toastContainer = document.createElement('div');
        toastContainer.className = `toast-container position-fixed bottom-0 end-0 p-3`;
        toastContainer.style.zIndex = "11";

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        toastContainer.appendChild(toast);
        document.body.appendChild(toastContainer);

        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Remove from DOM after hiding
        toast.addEventListener('hidden.bs.toast', () => {
            document.body.removeChild(toastContainer);
        });
    }
});