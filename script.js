const form = document.getElementById("registrationForm");
const message = document.getElementById("message");

form.addEventListener("submit", function(event) {

    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();

    if (phone.length !== 10 || isNaN(phone)) {
        message.style.display = "block";
        message.textContent = "Please enter a valid 10-digit phone number.";
        message.style.backgroundColor = "#ffe0e0";
        message.style.color = "#d00000";
        return;
    }

    message.style.display = "block";
    message.textContent = "Registration successful! Welcome, " + name + ".";
    message.style.backgroundColor = "#dff5e1";
    message.style.color = "#087f23";

    form.reset();
});