document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const nombreInput = document.querySelector('input[name="nombre"]');
    const emailInput = document.querySelector('input[name="email"]');
    const mensajeInput = document.querySelector('textarea[name="mensaje"]');
    
    const nombreError = document.getElementById('nombreError');
    const emailError = document.getElementById('emailError');
    const mensajeError = document.getElementById('mensajeError');

    // Funciones de validación
    function validarNombre(nombre) {
        return nombre.length >= 2 && nombre.length <= 100;
    }

    function validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    function validarMensaje(mensaje) {
        return mensaje.length >= 10 && mensaje.length <= 1000;
    }

    // Manejadores de eventos para validación en tiempo real
    nombreInput.addEventListener('input', function() {
        if (!validarNombre(this.value)) {
            nombreError.textContent = 'El nombre debe tener entre 2 y 100 caracteres';
            nombreError.style.display = 'block';
        } else {
            nombreError.style.display = 'none';
        }
    });

    emailInput.addEventListener('input', function() {
        if (!validarEmail(this.value)) {
            emailError.textContent = 'Por favor, introduce un email válido';
            emailError.style.display = 'block';
        } else {
            emailError.style.display = 'none';
        }
    });

    mensajeInput.addEventListener('input', function() {
        if (!validarMensaje(this.value)) {
            mensajeError.textContent = 'El mensaje debe tener entre 10 y 1000 caracteres';
            mensajeError.style.display = 'block';
        } else {
            mensajeError.style.display = 'none';
        }
    });

    // Validación en el envío del formulario
    form.addEventListener('submit', function(e) {
        let isValid = true;

        // Validar nombre
        if (!validarNombre(nombreInput.value)) {
            nombreError.textContent = 'El nombre debe tener entre 2 y 100 caracteres';
            nombreError.style.display = 'block';
            isValid = false;
        }

        // Validar email
        if (!validarEmail(emailInput.value)) {
            emailError.textContent = 'Por favor, introduce un email válido';
            emailError.style.display = 'block';
            isValid = false;
        }

        // Validar mensaje
        if (!validarMensaje(mensajeInput.value)) {
            mensajeError.textContent = 'El mensaje debe tener entre 10 y 1000 caracteres';
            mensajeError.style.display = 'block';
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });
});