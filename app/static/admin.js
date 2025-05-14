// Utility Functions
function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function toggleDropdown(dropdownId) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

function updateSelected(radio, toggleId) {
    const toggleButton = document.getElementById(toggleId).querySelector("span");
    toggleButton.textContent = radio.value || "All " + toggleId.replace("-filter-toggle", "").replace("-dropdown", "").split("-").map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");
    const dropdownId = toggleId.replace("-filter-toggle", "-dropdown");
    document.getElementById(dropdownId).style.display = "none";
}

window.onclick = function(event) {
    if (!event.target.matches(".dropdown-toggle")) {
        const dropdowns = document.querySelectorAll(".dropdown-content");
        dropdowns.forEach(dropdown => {
            if (dropdown.style.display === "block") {
                dropdown.style.display = "none";
            }
        });
    }
}

// Filter Functions
function applyDashboardFilters() {
    const statusFilterElements = document.querySelectorAll("#status-dropdown input[name='status']:checked");
    const statusFilter = Array.from(statusFilterElements)
                            .map(input => input.value)
                            .filter(value => value !== "");

    const typeFilterElements = document.querySelectorAll("#request-type-dropdown input[name='request_type']:checked");
    const typeFilter = Array.from(typeFilterElements)
                          .map(input => input.value)
                          .filter(value => value !== "");

    let queryParams = [];
    if (statusFilter.length > 0) {
        statusFilter.forEach(status => queryParams.push(`status=${encodeURIComponent(status)}`));
    }
    if (typeFilter.length > 0) {
        typeFilter.forEach(type => queryParams.push(`request_type=${encodeURIComponent(type)}`));
    }

    const queryString = queryParams.join("&");
    window.location.href = `/admin/dashboard${queryString ? "?" + queryString : ""}`;
}

function applyTicketFilters() {
    const statusFilterElements = document.querySelectorAll("#status-dropdown input[name='status']:checked");
    const statusFilter = Array.from(statusFilterElements)
                            .map(input => input.value)
                            .filter(value => value !== "");

    const typeFilterElements = document.querySelectorAll("#request-type-dropdown input[name='request_type']:checked");
    const typeFilter = Array.from(typeFilterElements)
                          .map(input => input.value)
                          .filter(value => value !== "");

    const assignedFilter = document.querySelector("#assigned-dropdown input[name='assigned_to']:checked")?.value;
    const creatorFilter = document.querySelector("#creator-dropdown input[name='creator_user']:checked")?.value;

    let queryParams = [];
    if (statusFilter.length > 0) {
        statusFilter.forEach(status => queryParams.push(`status=${encodeURIComponent(status)}`));
    }
    if (typeFilter.length > 0) {
        typeFilter.forEach(type => queryParams.push(`request_type=${encodeURIComponent(type)}`));
    }
    if (assignedFilter) queryParams.push(`assigned_to=${encodeURIComponent(assignedFilter)}`);
    if (creatorFilter) queryParams.push(`creator_user=${encodeURIComponent(creatorFilter)}`);

    const queryString = queryParams.join("&");
    window.location.href = `/admin/manage-tickets${queryString ? "?" + queryString : ""}`;
}

function applyUserFilters() {
    const roleFilterElements = document.querySelectorAll("#role-dropdown input[name='role']:checked");
    const roleFilter = Array.from(roleFilterElements)
                            .map(input => input.value)
                            .filter(value => value !== "");

    let queryParams = [];
    if (roleFilter.length > 0) {
        roleFilter.forEach(role => queryParams.push(`role=${encodeURIComponent(role)}`));
    }

    const queryString = queryParams.join("&");
    window.location.href = `/admin/manage-users${queryString ? "?" + queryString : ""}`;
}

function clearFilters(url) {
    window.location.href = url;
}

function initialiseTicketFilters() {
    const statusParams = new URLSearchParams(window.location.search).getAll("status");
    const typeParams = new URLSearchParams(window.location.search).getAll("request_type");

    document.querySelectorAll("#status-dropdown input[name='status']").forEach(radio => {
        if (statusParams.includes(radio.value)) {
            radio.checked = true;
        }
    });
    const selectedStatusesText = statusParams.length > 0 ? statusParams.join(", ") : "All";
    document.getElementById("status-filter-toggle").querySelector("span").textContent = selectedStatusesText;

    document.querySelectorAll("#request-type-dropdown input[name='request_type']").forEach(radio => {
        if (typeParams.includes(radio.value)) {
            radio.checked = true;
        }
    });
    const selectedTypesText = typeParams.length > 0 ? typeParams.join(", ") : "All";
    document.getElementById("request-type-filter-toggle").querySelector("span").textContent = selectedTypesText;
}

function initialiseUserFilters() {
    const roleParams = new URLSearchParams(window.location.search).getAll("role");

    document.querySelectorAll("#role-dropdown input[name='role']").forEach(radio => {
        if (roleParams.includes(radio.value)) {
            radio.checked = true;
        }
    });
    const selectedRolesText = roleParams.length > 0 ? roleParams.join(", ") : "All";
    document.getElementById("role-filter-toggle").querySelector("span").textContent = selectedRolesText;
}

// Popup Functions
document.addEventListener("DOMContentLoaded", function() {
    const editPopup = document.getElementById("editPopup");
    const deleteConfirmationPopup = document.getElementById("deleteConfirmationPopup");

    const closeEditPopupButton = editPopup.querySelector(".close-button");
    const closeDeletePopupButton = document.getElementById("closeDeletePopup");
    const cancelDeleteButton = document.getElementById("cancelDelete");

    // Edit functionality for tickets
    const editTicketForm = document.getElementById("editTicketForm");
    const ticketEditButtons = document.querySelectorAll(".ticket-edit-button");
    ticketEditButtons.forEach(button => {
        button.addEventListener("click", function() {
            const ticketId = this.dataset.ticketId;
            const requestType = this.dataset.requestType;
            const title = this.dataset.title;
            const description = this.dataset.description;
            const assignedTo = this.dataset.assignedTo;
            const status = this.dataset.status;

            editTicketForm.querySelector("#ticket_id").value = ticketId;
            editTicketForm.querySelector("#request_type").value = requestType;
            editTicketForm.querySelector("#title").value = title;
            editTicketForm.querySelector("#description").value = description;
            editTicketForm.querySelector("#assigned_to").value = assignedTo;
            editTicketForm.querySelector("#status").value = status;

            editPopup.style.display = "block";
        });
    });

    closeEditPopupButton.addEventListener("click", function() {
        editPopup.style.display = "none";
    });

    // Delete confirmation for tickets
    const ticketDeleteButtons = document.querySelectorAll(".ticket-delete-button");
    const deleteTicketIdInput = document.getElementById("delete_ticket_id");
    ticketDeleteButtons.forEach(button => {
        button.addEventListener("click", function() {
            const ticketId = this.dataset.ticketId;
            deleteTicketIdInput.value = ticketId;
            deleteConfirmationPopup.style.display = "block";
        });
    });

    closeDeletePopupButton.addEventListener("click", function() {
        deleteConfirmationPopup.style.display = "none";
    });

    cancelDeleteButton.addEventListener("click", function() {
        deleteConfirmationPopup.style.display = "none";
    });

    // Edit functionality for users
    const editUserForm = document.getElementById("editUserForm");
    const userEditButtons = document.querySelectorAll(".user-edit-button");
    userEditButtons.forEach(button => {
        button.addEventListener("click", function() {
            const userId = this.dataset.userId;
            const firstname = this.dataset.firstname;
            const surname = this.dataset.surname;
            const email = this.dataset.email;
            const role = this.dataset.role;

            editUserForm.querySelector("#user_id").value = userId;
            editUserForm.querySelector("#firstname").value = firstname;
            editUserForm.querySelector("#surname").value = surname;
            editUserForm.querySelector("#email").value = email;
            editUserForm.querySelector("#role").value = role;

            editPopup.style.display = "block";
        });
    });

    // Delete confirmation for users
    const userDeleteButtons = document.querySelectorAll(".user-delete-button");
    const deleteUserIdInput = document.getElementById("delete_user_id");
    userDeleteButtons.forEach(button => {
        button.addEventListener("click", function() {
            const userId = this.dataset.userId;
            deleteUserIdInput.value = userId;
            deleteConfirmationPopup.style.display = "block";
        });
    });

    closeDeletePopupButton.addEventListener("click", function() {
        deleteConfirmationPopup.style.display = "none";
    });

    cancelDeleteButton.addEventListener("click", function() {
        deleteConfirmationPopup.style.display = "none";
    });

    // Close popup when clicking outside
    window.addEventListener("click", function(event) {
        if (event.target == editPopup) {
            editPopup.style.display = "none";
        }
        if (event.target == deleteConfirmationPopup) {
            deleteConfirmationPopup.style.display = "none";
        }
    });

    // Search Functionality
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    const userTableRows = document.querySelectorAll(".user-table tbody tr");

    searchButton.addEventListener("click", function() {
        const searchTerm = searchInput.value.toLowerCase();
        userTableRows.forEach(row => {
            const firstName = row.querySelector(".firstname").textContent.toLowerCase();
            const surname = row.querySelector(".surname").textContent.toLowerCase();
            if (firstName.includes(searchTerm) || surname.includes(searchTerm)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});
