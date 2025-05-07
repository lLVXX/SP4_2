document.addEventListener('DOMContentLoaded', function() {
    // Simular envío de formularios (solo para mockup)
    const mockForms = document.querySelectorAll('form[id^="mock"]');
    
    mockForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Formulario enviado (simulación)');
            
            // Simular redirección después de registro
            if(form.id === 'mockRegisterForm') {
                setTimeout(() => {
                    window.location.href = '#'; // O la página a la que redirigirías
                }, 1500);
            }
        });
    });

    // Manejar el link "Inicia sesión" en registro
    const loginLink = document.querySelector('.login-link');
    if(loginLink) {
        loginLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/'; // Vuelve al home donde está el modal
        });
    }
});