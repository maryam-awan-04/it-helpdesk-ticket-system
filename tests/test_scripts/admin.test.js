/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");
const adminHtml = fs.readFileSync(path.resolve(__dirname, "admin_dom.html"), "utf8");
const {
    getQueryParam,
    toggleDropdown,
    updateSelected,
    applyDashboardFilters,
    applyTicketFilters,
    applyUserFilters,
    clearFilters,
    initialiseTicketFilters,
    initialiseUserFilters
} = require("../../app/static/admin.js");

describe("admin.js", () => {
  beforeEach(() => {
    document.body.innerHTML = adminHtml;
  });

  describe("Utility functions", () => {
    test("toggleDropdown toggles display style", () => {
      const dropdownId = "status-dropdown";
      const dropdown = document.getElementById(dropdownId);

      dropdown.style.display = "none";
      toggleDropdown(dropdownId);
      expect(dropdown.style.display).toBe("block");

      toggleDropdown(dropdownId);
      expect(dropdown.style.display).toBe("none");
    });

    test("updateSelected updates toggle button text and hides dropdown", () => {
      const radio = document.querySelector("#status-dropdown input[name='status']");
      radio.value = "Open";
      radio.checked = true;

      const toggleId = "status-filter-toggle";
      const toggleButtonSpan = document.getElementById(toggleId).querySelector("span");

      toggleButtonSpan.textContent = "All";
      document.getElementById("status-dropdown").style.display = "block";

      updateSelected(radio, toggleId);

      expect(toggleButtonSpan.textContent).toBe("Open");
      expect(document.getElementById("status-dropdown").style.display).toBe("none");
    });
  });

  describe("Filter functions", () => {
    beforeEach(() => {
      delete window.location;
      window.location = { href: "" };
    });

    test("applyDashboardFilters sets correct URL with filters", () => {
      const statusInput = document.querySelector("#status-dropdown input[value='Open']");
      const typeInput = document.querySelector("#request-type-dropdown input[value='Access Request']");
      statusInput.checked = true;
      typeInput.checked = true;

      applyDashboardFilters();

      expect(window.location.href).toBe("/admin/dashboard?status=Open&request_type=Access%20Request");
    });

    test("applyTicketFilters sets correct URL with filters", () => {
      const statusInput = document.querySelector("#status-dropdown input[value='Open']");
      const typeInput = document.querySelector("#request-type-dropdown input[value='Access Request']");
      const assignedInput = document.querySelector("#assigned-dropdown input[value='user1']");
      const creatorInput = document.querySelector("#creator-dropdown input[value='user2']");
      statusInput.checked = true;
      typeInput.checked = true;
      assignedInput.checked = true;
      creatorInput.checked = true;

      applyTicketFilters();

      expect(window.location.href).toBe(
        "/admin/manage-tickets?status=Open&request_type=Access%20Request&assigned_to=user1&creator_user=user2"
      );
    });

    test("applyUserFilters sets correct URL with roles", () => {
      const roleInput = document.querySelector("#role-dropdown input[value='Admin']");
      roleInput.checked = true;

      applyUserFilters();

      expect(window.location.href).toBe("/admin/manage-users?role=Admin");
    });

    test("clearFilters sets URL correctly", () => {
      clearFilters("/admin/manage-users");
      expect(window.location.href).toBe("/admin/manage-users");
    });
  });

  describe("Initialisation functions", () => {
    test("initialiseTicketFilters sets checkboxes and toggle text", () => {
      const url = "?status=Open&status=Closed";
      delete window.location;
      window.location = { search: url };

      initialiseTicketFilters();

      expect(
        document.querySelector("#status-dropdown input[value='Open']").checked
      ).toBe(true);
      expect(
        document.querySelector("#status-dropdown input[value='Closed']").checked
      ).toBe(true);

      expect(
        document.getElementById("status-filter-toggle").querySelector("span").textContent
      ).toBe("Open, Closed");
    });

    test("initialiseUserFilters sets checkboxes and toggle text", () => {
      const url = "?role=Admin&role=User";
      delete window.location;
      window.location = { search: url };

      initialiseUserFilters();

      expect(document.querySelector("#role-dropdown input[value='Admin']").checked).toBe(true);
      expect(document.querySelector("#role-dropdown input[value='User']").checked).toBe(true);

      expect(
        document.getElementById("role-filter-toggle").querySelector("span").textContent
      ).toBe("Admin, User");
    });
  });

  describe("Popup functionality", () => {
    beforeEach(() => {
      document.dispatchEvent(new Event("DOMContentLoaded"));
    });

    test("edit ticket button opens edit popup with prefilled form", () => {
      const editPopup = document.getElementById("editPopup");
      expect(editPopup.style.display).toBe("none");

      const button = document.querySelector(".ticket-edit-button");
      button.click();

      expect(editPopup.style.display).toBe("block");

      const form = document.getElementById("editTicketForm");
      expect(form.querySelector("#ticket_id").value).toBe("123");
      expect(form.querySelector("#request_type").value).toBe("Access Request");
      expect(form.querySelector("#title").value).toBe("Issue Title");
      expect(form.querySelector("#description").value).toBe("Issue description");
      expect(form.querySelector("#assigned_to").value).toBe("user1");
      expect(form.querySelector("#status").value).toBe("Open");
    });

    test("close edit popup button hides popup", () => {
      const editPopup = document.getElementById("editPopup");
      const closeButton = editPopup.querySelector(".close-button");
      editPopup.style.display = "block";

      closeButton.click();

      expect(editPopup.style.display).toBe("none");
    });

    test("delete ticket button opens delete confirmation popup with ticket id", () => {
      const deletePopup = document.getElementById("deleteConfirmationPopup");
      const deleteTicketInput = document.getElementById("delete_ticket_id");
      expect(deletePopup.style.display).toBe("none");

      const button = document.querySelector(".ticket-delete-button");
      button.click();

      expect(deletePopup.style.display).toBe("block");
      expect(deleteTicketInput.value).toBe("123");
    });

    test("close delete popup and cancel delete buttons hide delete popup", () => {
      const deletePopup = document.getElementById("deleteConfirmationPopup");
      const closeDelete = document.getElementById("closeDeletePopup");
      const cancelDelete = document.getElementById("cancelDelete");

      deletePopup.style.display = "block";

      closeDelete.click();
      expect(deletePopup.style.display).toBe("none");

      deletePopup.style.display = "block";
      cancelDelete.click();
      expect(deletePopup.style.display).toBe("none");
    });

    test("edit user button opens edit popup with user form prefilled", () => {
      const editPopup = document.getElementById("editPopup");
      const button = document.querySelector(".user-edit-button");
      button.click();

      expect(editPopup.style.display).toBe("block");

      const form = document.getElementById("editUserForm");
      expect(form.querySelector("#user_id").value).toBe("u123");
      expect(form.querySelector("#firstname").value).toBe("John");
      expect(form.querySelector("#surname").value).toBe("Doe");
      expect(form.querySelector("#email").value).toBe("john@example.com");
      expect(form.querySelector("#role").value).toBe("Admin");
    });

    test("delete user button opens delete confirmation popup with user id", () => {
      const deletePopup = document.getElementById("deleteConfirmationPopup");
      const deleteUserInput = document.getElementById("delete_user_id");

      const button = document.querySelector(".user-delete-button");
      button.click();

      expect(deletePopup.style.display).toBe("block");
      expect(deleteUserInput.value).toBe("u123");
    });

    test("clicking outside popups hides them", () => {
      const editPopup = document.getElementById("editPopup");
      const deletePopup = document.getElementById("deleteConfirmationPopup");

      editPopup.style.display = "block";
      deletePopup.style.display = "block";

      editPopup.click();
      expect(editPopup.style.display).toBe("none");

      deletePopup.click();
      expect(deletePopup.style.display).toBe("none");
    });
  });

  describe("Search functionality", () => {
    beforeEach(() => {
      document.dispatchEvent(new Event("DOMContentLoaded"));
    });

    test("search button filters table rows by first or surname", () => {
      const searchInput = document.getElementById("search-input");
      const searchButton = document.getElementById("search-button");

      searchInput.value = "john";
      searchButton.click();

      const rows = document.querySelectorAll(".user-table tbody tr");

      expect(rows[0].style.display).toBe("");
      expect(rows[1].style.display).toBe("none");

      searchInput.value = "smith";
      searchButton.click();

      expect(rows[0].style.display).toBe("none");
      expect(rows[1].style.display).toBe("");

      searchInput.value = "";
      searchButton.click();

      expect(rows[0].style.display).toBe("");
      expect(rows[1].style.display).toBe("");
    });
  });

  describe("Window onclick closes dropdowns", () => {
    test("click outside dropdown closes all dropdowns", () => {
      const statusDropdown = document.getElementById("status-dropdown");
      const typeDropdown = document.getElementById("request-type-dropdown");

      statusDropdown.style.display = "block";
      typeDropdown.style.display = "block";

      document.body.click();
      expect(statusDropdown.style.display).toBe("none");
      expect(typeDropdown.style.display).toBe("none");
    });

    test("click on dropdown toggle does not close dropdowns", () => {
      const statusDropdown = document.getElementById("status-dropdown");
      statusDropdown.style.display = "block";

      const toggleButton = document.createElement("button");
      toggleButton.classList.add("dropdown-toggle");

      toggleButton.click();
      expect(statusDropdown.style.display).toBe("block");
    });
  });
});
