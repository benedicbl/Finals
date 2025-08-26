document.addEventListener('DOMContentLoaded', function() {

    const actionButtons = document.querySelectorAll('.action-btn');

    actionButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            closeAllDropdowns(this);
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('action-dropdown')) {
                dropdown.classList.toggle('show');
            }
        });
    });

    function closeAllDropdowns(exceptButton = null) {
        document.querySelectorAll('.action-dropdown.show').forEach(openDropdown => {
            if (exceptButton === null || !exceptButton.nextElementSibling.isSameNode(openDropdown)) {
                openDropdown.classList.remove('show');
            }
        });
    }

    window.addEventListener('click', function(event) {
        if (!event.target.closest('.action-btn')) {
            closeAllDropdowns();
        }
    });


    const checkAllCheckbox = document.querySelector('thead input[type="checkbox"]');
    const itemCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]');

    if (checkAllCheckbox && itemCheckboxes.length > 0) {
        // Event ketika checkbox "check all" di klik
        checkAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });

        // Event untuk memantau jika semua checkbox item terpilih, maka "check all" juga terpilih
        itemCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const allChecked = Array.from(itemCheckboxes).every(item => item.checked);
                checkAllCheckbox.checked = allChecked;
            });
        });
    }
});