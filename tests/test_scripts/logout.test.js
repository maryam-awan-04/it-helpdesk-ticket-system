/**
 * @jest-environment jsdom
 */

beforeEach(() => {
  document.body.innerHTML = `
    <div id="customAlert" data-logout-url="/logout" style="display: none;">
      <p id="alertMessage"></p>
      <button id="alertYesButton">Yes</button>
      <button id="alertNoButton">No</button>
    </div>
    <a href="#" class="logout-button">Logout</a>
  `;

  require('../../app/static/logout.js');

  document.dispatchEvent(new Event("DOMContentLoaded"));
});

test("displays alert on logout button click", () => {
  document.querySelector(".logout-button").click();
  expect(document.getElementById("customAlert").style.display).toBe("flex");
  expect(document.getElementById("alertMessage").textContent).toBe("Are you sure you want to sign out?");
});

test("clicking 'No' hides the alert", () => {
  document.querySelector(".logout-button").click();
  document.getElementById("alertNoButton").click();
  expect(document.getElementById("customAlert").style.display).toBe("none");
});

test("clicking 'Yes' redirects to logout URL", () => {
  delete window.location;
  window.location = { href: "" };

  document.querySelector(".logout-button").click();
  document.getElementById("alertYesButton").click();

  expect(window.location.href).toBe("/logout");
});
