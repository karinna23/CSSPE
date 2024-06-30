document.addEventListener('DOMContentLoaded', () => {
    // ---------- Toggle Show Password ----------
    const passInput = document.querySelector('.referee-login .pass-cont #password'),
        passToggleBtn = passInput.nextElementSibling,
        passIcon = passToggleBtn.firstElementChild;

    passToggleBtn.onclick = () => {
        if (passIcon.src.includes('eyeslash')) {
            passInput.type = 'password';
            passIcon.src = "/static/img/icons/eye.svg";
        }
        else {
            passInput.type = 'text';
            passIcon.src = "/static/img/icons/eyeslash.svg";
        }
    }
});