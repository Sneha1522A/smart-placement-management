const loginForm = document.getElementById("loginForm");

const email = document.getElementById("email");
const password = document.getElementById("password");

const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");

const loginMessage = document.getElementById("loginMessage");


loginForm.addEventListener("submit", function (event) {

    // Prevent page refresh
    event.preventDefault();

    // Clear previous messages
    emailError.textContent = "";
    passwordError.textContent = "";
    loginMessage.textContent = "";

    let isValid = true;


    // =========================
    // EMAIL VALIDATION
    // =========================

    if (email.value.trim() === "") {

        emailError.textContent =
            "Student email is required.";

        isValid = false;

    }
    else if (!isValidEmail(email.value.trim())) {

        emailError.textContent =
            "Please enter a valid email address.";

        isValid = false;
    }


    // =========================
    // PASSWORD VALIDATION
    // =========================

    if (password.value.trim() === "") {

        passwordError.textContent =
            "Password is required.";

        isValid = false;

    }

    // Minimum 8 characters
    else if (password.value.length < 8) {

        passwordError.textContent =
            "Password must be at least 8 characters.";

        isValid = false;
    }

    // At least one capital letter
    else if (!/[A-Z]/.test(password.value)) {

        passwordError.textContent =
            "Password must contain at least one capital letter.";

        isValid = false;
    }

    // At least one number
    else if (!/[0-9]/.test(password.value)) {

        passwordError.textContent =
            "Password must contain at least one number.";

        isValid = false;
    }

    // At least one special character
    else if (!/[!@#$%^&*(),.?":{}|<>_\-\\[\]\/~`+=;]/.test(password.value)) {

        passwordError.textContent =
            "Password must contain at least one special character.";

        isValid = false;
    }


    // =========================
    // FINAL RESULT
    // =========================

    if (isValid) {

        loginMessage.textContent =
            "Login details are valid.";

        loginMessage.style.color = "green";

    }

});


// =========================
// EMAIL FORMAT VALIDATION
// =========================

function isValidEmail(email) {

    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return emailPattern.test(email);
}