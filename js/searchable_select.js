document.addEventListener('DOMContentLoaded', function() {
    const selectFields = document.querySelectorAll('.searchable-select');

    selectFields.forEach(function(select) {
        // Create search input
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search...';
        searchInput.className = 'form-control mb-2 searchable-input';

        // Insert search input before select
        select.parentNode.insertBefore(searchInput, select);

        // Add search functionality
        searchInput.addEventListener('input', function(e) {
            const searchText = e.target.value.toLowerCase();
            const options = select.querySelectorAll('option');

            options.forEach(function(option) {
                const text = option.textContent.toLowerCase();
                if (text.includes(searchText)) {
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                }
            });
        });
    });
});