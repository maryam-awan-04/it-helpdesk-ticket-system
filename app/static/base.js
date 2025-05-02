document.addEventListener("DOMContentLoaded", function () {
    const logoutButtons = document.querySelectorAll(".logout-button");
    const customAlert = document.getElementById("customAlert");
    const alertMessage = document.getElementById("alertMessage");
    const alertYesButton = document.getElementById("alertYesButton");
    const alertNoButton = document.getElementById("alertNoButton");

    logoutButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            if (customAlert) {
                alertMessage.textContent = "Are you sure you want to sign out?";
                customAlert.style.display = "flex";
            }
        });
    });

    if (alertYesButton && alertNoButton) {
        alertYesButton.addEventListener("click", function() {
            window.location.href = "{{ url_for('auth.logout') }}";
        });

        alertNoButton.addEventListener("click", function() {
            if (customAlert) {
                customAlert.style.display = "none";
            }
        });
    }
});
