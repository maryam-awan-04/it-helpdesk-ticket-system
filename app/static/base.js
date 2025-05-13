document.addEventListener("DOMContentLoaded", function () {
    const logoutButtons = document.querySelectorAll(".logout-button");
    const customAlert = document.getElementById("customAlert");
    const alertMessage = document.getElementById("alertMessage");
    const alertYesButton = document.getElementById("alertYesButton");
    const alertNoButton = document.getElementById("alertNoButton");

    logoutButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            console.log("Logout button clicked");
            if (customAlert) {
                alertMessage.textContent = "Are you sure you want to sign out?";
                customAlert.style.display = "flex";
            }
        });
    });

    if (alertYesButton && alertNoButton) {
        const logoutURL = customAlert.dataset.logoutUrl;

        alertYesButton.addEventListener("click", function() {
            window.location.href = logoutURL;
        });

        alertNoButton.addEventListener("click", function() {
            if (customAlert) {
                customAlert.style.display = "none";
            }
        });
    }
});
