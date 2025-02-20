document.querySelector('.gestion-form').addEventListener('submit', function() {
    const button = this.querySelector('button');
    const spinner = button.querySelector('.cargando');
    button.disabled = true;
    spinner.style.display = 'inline-block';
});