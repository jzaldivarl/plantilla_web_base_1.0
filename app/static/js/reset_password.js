document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const submitButton = form.querySelector('button[type="submit"]');

    // Validar si las contraseñas coinciden
    function validatePasswords() {
        if (passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.setCustomValidity('Las contraseñas no coinciden.');
        } else {
            confirmPasswordInput.setCustomValidity('');
        }
    }

    // Escuchar cambios en los campos de contraseña
    passwordInput.addEventListener('input', validatePasswords);
    confirmPasswordInput.addEventListener('input', validatePasswords);

    // Validar el formulario antes de enviarlo
    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        form.classList.add('was-validated');
    });

    // Mostrar u ocultar las contraseñas
    const togglePasswordVisibility = document.createElement('button');
    togglePasswordVisibility.type = 'button';
    togglePasswordVisibility.textContent = '👁️';
    togglePasswordVisibility.className = 'btn btn-outline-secondary btn-sm';
    togglePasswordVisibility.style.position = 'absolute';
    togglePasswordVisibility.style.right = '10px';
    togglePasswordVisibility.style.top = '50%';
    togglePasswordVisibility.style.transform = 'translateY(-50%)';

    const passwordFieldContainer = passwordInput.parentNode;
    passwordFieldContainer.style.position = 'relative';
    passwordFieldContainer.appendChild(togglePasswordVisibility);

    togglePasswordVisibility.addEventListener('click', function () {
        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type;
        confirmPasswordInput.type = type;
        this.textContent = type === 'password' ? '👁️' : '🙈';
    });
});
