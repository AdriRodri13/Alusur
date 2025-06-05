// ========== CRUD JAVASCRIPT COMPARTIDO ==========

// Variables globales
let currentEditId = null;

// ========== INICIALIZACIÓN ==========
document.addEventListener('DOMContentLoaded', function() {
    initializeCRUD();
});

function initializeCRUD() {
    // Inicializar búsqueda
    initializeSearch();
    
    // Inicializar filtros
    initializeFilters();
    
    // Inicializar vista previa de imágenes
    initializeImagePreviews();
    
    // Inicializar tooltips
    initializeTooltips();
    
    // Manejar envío de formularios
    initializeFormSubmission();
}

// ========== BÚSQUEDA Y FILTROS ==========
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filterTable();
        });
    }
}

function initializeFilters() {
    const filters = document.querySelectorAll('select[id$="Filter"]');
    filters.forEach(filter => {
        filter.addEventListener('change', function() {
            filterTable();
        });
    });
}

function filterTable() {
    const searchValue = document.getElementById('searchInput')?.value.toLowerCase() || '';
    const table = document.querySelector('.crud-table tbody');
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matchesSearch = text.includes(searchValue);
        
        // Aquí puedes agregar más lógica de filtrado según los filtros específicos
        row.style.display = matchesSearch ? '' : 'none';
    });
}

function clearFilters() {
    // Limpiar búsqueda
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = '';
    }
    
    // Limpiar filtros select
    const filters = document.querySelectorAll('select[id$="Filter"]');
    filters.forEach(filter => {
        filter.value = '';
    });
    
    // Refiltar tabla
    filterTable();
}

// ========== GESTIÓN DE MODALES ==========
function openCreateModalGeneric() {
    currentEditId = null;
    
    // Limpiar formulario
    const form = document.querySelector('form[id$="Form"]');
    if (form) {
        form.reset();
        
        // Limpiar ID oculto
        const idField = form.querySelector('input[type="hidden"][id$="Id"]');
        if (idField) {
            idField.value = '';
        }
    }
    
    // Actualizar título del modal
    const modalTitle = document.getElementById('modalTitle');
    if (modalTitle) {
        const modelName = CRUD_CONFIG.modelName;
        modalTitle.textContent = `Nuevo ${getModelDisplayName(modelName)}`;
    }
    
    // Actualizar botón de guardar
    const saveButtonText = document.getElementById('saveButtonText');
    if (saveButtonText) {
        const modelName = CRUD_CONFIG.modelName;
        saveButtonText.textContent = `Guardar ${getModelDisplayName(modelName)}`;
    }
    
    // Limpiar vista previa de imágenes
    clearImagePreviews();
}

function editItem(id) {
    currentEditId = id;
    
    // Construir URL para obtener datos
    const url = CRUD_CONFIG.ajaxUrls.get.replace('0', id);
    
    // Realizar petición AJAX
    fetch(url, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            populateEditForm(data.data);
            
            // Actualizar título del modal
            const modalTitle = document.getElementById('modalTitle');
            if (modalTitle) {
                const modelName = CRUD_CONFIG.modelName;
                modalTitle.textContent = `Editar ${getModelDisplayName(modelName)}`;
            }
            
            // Actualizar botón de guardar
            const saveButtonText = document.getElementById('saveButtonText');
            if (saveButtonText) {
                const modelName = CRUD_CONFIG.modelName;
                saveButtonText.textContent = `Actualizar ${getModelDisplayName(modelName)}`;
            }
            
            // Mostrar modal
            const modalId = `${CRUD_CONFIG.modelName}Modal`;
            const modal = new bootstrap.Modal(document.getElementById(modalId));
            modal.show();
        } else {
            showAlert('Error al cargar los datos: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error de conexión', 'danger');
    });
}

function populateEditForm(data) {
    const form = document.querySelector('form[id$="Form"]');
    if (!form) return;
    
    // Llenar campos del formulario
    Object.keys(data).forEach(key => {
        const field = form.querySelector(`[name="${key}"], #${key}`);
        if (field) {
            if (field.type === 'checkbox') {
                field.checked = data[key];
            } else if (field.type === 'file') {
                // No llenar campos de archivo, solo mostrar vista previa si existe
                if (data[key] && data[key] !== '') {
                    showImagePreview(field, data[key]);
                }
            } else {
                field.value = data[key] || '';
            }
        }
    });
}

function viewItem(id) {
    // Construir URL para obtener datos
    const url = CRUD_CONFIG.ajaxUrls.get.replace('0', id);
    
    // Realizar petición AJAX
    fetch(url, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            populateViewModal(data.data);
            
            // Mostrar modal de vista
            const modal = new bootstrap.Modal(document.getElementById('viewModal'));
            modal.show();
        } else {
            showAlert('Error al cargar los datos: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error de conexión', 'danger');
    });
}

function populateViewModal(data) {
    // Llenar campos de vista
    console.log('Datos recibidos:', data);

    Object.keys(data).forEach(key => {
        const viewElement = document.getElementById(`view${capitalizeFirst(key)}`);
        if (viewElement) {
            if (key.includes('imagen') || key.includes('logo')) {
                // Manejar imágenes
                if (data[key] && data[key] !== '') {
                    viewElement.innerHTML = `<img src="${data[key]}" alt="Imagen" class="img-fluid rounded">`;
                } else {
                    viewElement.innerHTML = '<i class="fas fa-image"></i><span>Sin imagen</span>';
                }
            } else if (typeof data[key] === 'boolean') {
                // Manejar booleanos
                viewElement.textContent = data[key] ? 'Sí' : 'No';
            } else {
                viewElement.textContent = data[key] || 'No especificado';
            }
        }
    });
}

function deleteItem(id) {
    const modelName = getModelDisplayName(CRUD_CONFIG.modelName);
    
    // Confirmar eliminación
    if (!confirm(`¿Estás seguro de que deseas eliminar este ${modelName.toLowerCase()}? Esta acción no se puede deshacer.`)) {
        return;
    }
    
    // Construir URL para eliminar
    const url = CRUD_CONFIG.ajaxUrls.delete.replace('0', id);
    
    // Realizar petición AJAX
    fetch(url, {
        method: 'DELETE',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            if (data.reload) {
                setTimeout(() => {
                    location.reload();
                }, 1500);
            }
        } else {
            showAlert('Error al eliminar: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error de conexión', 'danger');
    });
}

// ========== ENVÍO DE FORMULARIOS ==========
function initializeFormSubmission() {
    const form = document.querySelector('form[id$="Form"]');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            saveItem();
        });
    }
}

function saveItem() {
    const form = document.querySelector('form[id$="Form"]');
    if (!form) return;
    
    // Validar formulario
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    // Deshabilitar botón de guardar
    const saveButton = document.getElementById('saveButton');
    if (saveButton) {
        saveButton.disabled = true;
        saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
    }
    
    // Preparar datos del formulario
    const formData = new FormData(form);
    
    // Realizar petición AJAX
    fetch(CRUD_CONFIG.ajaxUrls.save, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            
            // Cerrar modal
            const modalId = `${CRUD_CONFIG.modelName}Modal`;
            const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
            if (modal) {
                modal.hide();
            }
            
            // Recargar página si es necesario
            if (data.reload) {
                setTimeout(() => {
                    location.reload();
                }, 1500);
            }
        } else {
            showAlert('Error al guardar: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error de conexión', 'danger');
    })
    .finally(() => {
        // Rehabilitar botón de guardar
        if (saveButton) {
            saveButton.disabled = false;
            const modelName = CRUD_CONFIG.modelName;
            const actionText = currentEditId ? 'Actualizar' : 'Guardar';
            saveButton.innerHTML = `<i class="fas fa-save"></i> ${actionText} ${getModelDisplayName(modelName)}`;
        }
    });
}

// ========== VISTA PREVIA DE IMÁGENES ==========
function initializeImagePreviews() {
    const imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(input => {
        if (input.accept && input.accept.includes('image')) {
            input.addEventListener('change', function() {
                handleImagePreview(this);
            });
        }
    });
}

function handleImagePreview(input) {
    const previewId = input.id + 'Preview';
    const preview = document.getElementById(previewId);
    
    if (input.files && input.files[0] && preview) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Vista previa" class="img-fluid rounded">`;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function showImagePreview(input, imageUrl) {
    const previewId = input.id + 'Preview';
    const preview = document.getElementById(previewId);
    
    if (preview && imageUrl) {
        preview.innerHTML = `<img src="${imageUrl}" alt="Imagen actual" class="img-fluid rounded">`;
    }
}

function clearImagePreviews() {
    const previews = document.querySelectorAll('.image-preview');
    previews.forEach(preview => {
        const iconClass = preview.closest('form').querySelector('i').className;
        preview.innerHTML = `<i class="${iconClass}"></i><span>Sin imagen</span>`;
    });
}

// ========== TOOLTIPS ==========
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ========== ALERTAS ==========
function showAlert(message, type = 'info') {
    // Crear elemento de alerta
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)}"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Buscar contenedor de alertas o crear uno
    let alertContainer = document.querySelector('.alerts-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'alerts-container';
        
        // Insertar al principio del contenido principal
        const mainContent = document.querySelector('.admin-content');
        if (mainContent) {
            mainContent.insertBefore(alertContainer, mainContent.firstChild);
        }
    }
    
    // Agregar alerta
    alertContainer.appendChild(alertDiv);
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// ========== UTILIDADES ==========
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function getModelDisplayName(modelName) {
    const displayNames = {
        'servicio': 'Servicio',
        'presentacion': 'Texto de Presentación',
        'proyecto': 'Proyecto'
    };
    return displayNames[modelName] || modelName;
}

// ========== EVENTOS GLOBALES ==========
document.addEventListener('hidden.bs.modal', function (event) {
    // Limpiar formulario cuando se cierra un modal
    const form = event.target.querySelector('form');
    if (form) {
        form.reset();
        form.classList.remove('was-validated');
        clearImagePreviews();
    }
    
    // Resetear ID actual
    currentEditId = null;
});