// =======================================================================
// SISTEMA DE GESTIÓN DE INVENTARIOS - MAESTRANZAS UNIDOS
// =======================================================================

class InventoryManager {
    constructor() {
        this.currentUser = null;
        this.inventory = [];
        this.categories = [
            'Herramientas',
            'Materiales',
            'Equipos',
            'Repuestos',
            'Consumibles',
            'Seguridad',
            'Otros'
        ];
        this.users = [
            { username: 'admin', password: 'admin123', name: 'Administrador', role: 'admin' },
            { username: 'usuario', password: 'user123', name: 'Usuario General', role: 'user' }
        ];
        
        this.init();
    }

    init() {
        this.loadData();
        this.loadUsers();
        this.setupEventListeners();
        this.checkAuth();
    }

    // =======================================================================
    // SISTEMA DE AUTENTICACIÓN
    // =======================================================================
    
    checkAuth() {
        const savedUser = localStorage.getItem('currentUser');
        if (savedUser) {
            this.currentUser = JSON.parse(savedUser);
            this.showMainContent();
            this.updateUserDisplay();
        } else {
            this.showLoginModal();
        }
    }

    login(username, password) {
        const user = this.users.find(u => u.username === username && u.password === password);
        if (user) {
            this.currentUser = user;
            localStorage.setItem('currentUser', JSON.stringify(user));
            this.showMainContent();
            this.updateUserDisplay();
            this.showNotification('¡Bienvenido!', `Hola ${user.name}`, 'success');
            return true;
        }
        return false;
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('currentUser');
        this.showLoginModal();
        this.showNotification('Sesión cerrada', 'Has cerrado sesión correctamente', 'success');
    }

    // =======================================================================
    // GESTIÓN DE DATOS
    // =======================================================================

    loadData() {
        const savedInventory = localStorage.getItem('inventory');
        this.inventory = savedInventory ? JSON.parse(savedInventory) : [];
        
        // Datos de ejemplo si no hay inventario
        if (this.inventory.length === 0) {
            this.inventory = [
                {
                    id: 1,
                    sku: 'HERR-001',
                    name: 'Taladro Eléctrico',
                    category: 'Herramientas',
                    location: 'Almacén A - Estante 1',
                    stock: 15,
                    minimum: 5,
                    price: 89.99,
                    supplier: 'Ferretería Central',
                    description: 'Taladro eléctrico de 18V con batería recargable',
                    createdAt: new Date().toISOString(),
                    updatedAt: new Date().toISOString()
                },
                {
                    id: 2,
                    sku: 'MAT-001',
                    name: 'Tornillos M6x20',
                    category: 'Materiales',
                    location: 'Almacén B - Caja 3',
                    stock: 3,
                    minimum: 10,
                    price: 0.25,
                    supplier: 'Distribuidora Industrial',
                    description: 'Tornillos métricos M6x20mm cabeza hexagonal',
                    createdAt: new Date().toISOString(),
                    updatedAt: new Date().toISOString()
                }
            ];
            this.saveData();
        }
    }

    saveData() {
        localStorage.setItem('inventory', JSON.stringify(this.inventory));
    }

    // =======================================================================
    // OPERACIONES CRUD
    // =======================================================================

    addItem(itemData) {
        const newItem = {
            id: Date.now(),
            ...itemData,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        this.inventory.push(newItem);
        this.saveData();
        this.renderInventory();
        this.updateStats();
        this.showNotification('Ítem agregado', `${itemData.name} ha sido agregado al inventario`, 'success');
    }

    updateItem(id, itemData) {
        const index = this.inventory.findIndex(item => item.id === id);
        if (index !== -1) {
            this.inventory[index] = {
                ...this.inventory[index],
                ...itemData,
                updatedAt: new Date().toISOString()
            };
            this.saveData();
            this.renderInventory();
            this.updateStats();
            this.showNotification('Ítem actualizado', `${itemData.name} ha sido actualizado`, 'success');
        }
    }

    deleteItem(id) {
        const item = this.inventory.find(item => item.id === id);
        if (item && confirm(`¿Estás seguro de que deseas eliminar "${item.name}"?`)) {
            this.inventory = this.inventory.filter(item => item.id !== id);
            this.saveData();
            this.renderInventory();
            this.updateStats();
            this.showNotification('Ítem eliminado', `${item.name} ha sido eliminado del inventario`, 'success');
        }
    }

    // =======================================================================
    // MOVIMIENTOS DE STOCK
    // =======================================================================

    adjustStock(id, quantity, reason) {
        const item = this.inventory.find(item => item.id === id);
        if (item) {
            const newStock = Math.max(0, item.stock + quantity);
            item.stock = newStock;
            item.updatedAt = new Date().toISOString();
            
            // Registrar movimiento
            const movement = {
                id: Date.now(),
                itemId: id,
                itemName: item.name,
                quantity: quantity,
                reason: reason,
                timestamp: new Date().toISOString(),
                user: this.currentUser.name
            };
            
            this.saveMovement(movement);
            this.saveData();
            this.renderInventory();
            this.updateStats();
            
            const action = quantity > 0 ? 'agregado' : 'retirado';
            this.showNotification('Stock ajustado', `${Math.abs(quantity)} unidades ${action} de ${item.name}`, 'success');
        }
    }

    saveMovement(movement) {
        const movements = JSON.parse(localStorage.getItem('movements') || '[]');
        movements.push(movement);
        localStorage.setItem('movements', JSON.stringify(movements));
    }

    // =======================================================================
    // RENDERIZADO
    // =======================================================================

    renderInventory() {
        const tbody = document.getElementById('inventory-tbody');
        const searchTerm = document.getElementById('search-input').value.toLowerCase();
        const categoryFilter = document.getElementById('filter-category').value;
        
        let filteredItems = this.inventory.filter(item => {
            const matchesSearch = item.name.toLowerCase().includes(searchTerm) || 
                                item.sku.toLowerCase().includes(searchTerm) ||
                                item.location.toLowerCase().includes(searchTerm);
            const matchesCategory = !categoryFilter || item.category === categoryFilter;
            return matchesSearch && matchesCategory;
        });

        tbody.innerHTML = '';

        filteredItems.forEach(item => {
            const tr = document.createElement('tr');
            const stockStatus = this.getStockStatus(item);
            
            if (stockStatus === 'out') tr.classList.add('out-of-stock');
            else if (stockStatus === 'low') tr.classList.add('low-stock');

            tr.innerHTML = `
                <td><strong>${item.sku}</strong></td>
                <td>${item.name}</td>
                <td>${item.category}</td>
                <td>${item.location}</td>
                <td><strong>${item.stock}</strong></td>
                <td>${item.minimum}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td><span class="stock-status ${stockStatus}">${this.getStockStatusText(stockStatus)}</span></td>
                <td>
                    <div class="action-buttons">
                        <button class="action-btn btn-success" onclick="app.showMovementModal(${item.id})" title="Ajustar Stock">
                            <i class="fas fa-exchange-alt"></i>
                        </button>
                        <button class="action-btn btn-primary" onclick="app.editItem(${item.id})" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn btn-danger" onclick="app.deleteItem(${item.id})" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    updateStats() {
        const totalItems = this.inventory.length;
        const lowStockItems = this.inventory.filter(item => 
            item.stock <= item.minimum && item.minimum > 0
        ).length;
        const outOfStockItems = this.inventory.filter(item => item.stock === 0).length;
        const totalValue = this.inventory.reduce((sum, item) => sum + (item.stock * item.price), 0);

        document.getElementById('total-items').textContent = totalItems;
        document.getElementById('low-stock-count').textContent = lowStockItems;
        document.getElementById('out-of-stock-count').textContent = outOfStockItems;
        document.getElementById('total-value').textContent = `$${totalValue.toFixed(2)}`;

        // Mostrar alertas de stock bajo
        this.showLowStockAlerts();
    }

    getStockStatus(item) {
        if (item.stock === 0) return 'out';
        if (item.stock <= item.minimum && item.minimum > 0) return 'low';
        return 'normal';
    }

    getStockStatusText(status) {
        const statusTexts = {
            normal: 'Normal',
            low: 'Bajo',
            out: 'Sin Stock'
        };
        return statusTexts[status] || 'Normal';
    }

    showLowStockAlerts() {
        const lowStockItems = this.inventory.filter(item => 
            item.stock <= item.minimum && item.minimum > 0
        );

        if (lowStockItems.length > 0) {
            const message = `Stock bajo en: ${lowStockItems.map(item => item.name).join(', ')}`;
            this.showNotification('Alerta de Stock', message, 'warning');
        }
    }

    // =======================================================================
    // MODALES
    // =======================================================================

    showLoginModal() {
        document.getElementById('login-modal').classList.add('show');
        document.getElementById('main-content').style.display = 'none';
    }

    showMainContent() {
        document.getElementById('login-modal').classList.remove('show');
        document.getElementById('main-content').style.display = 'block';
        this.renderInventory();
        this.updateStats();
        this.populateCategories();
        this.checkAdminPermissions();
    }

    showItemModal(isEdit = false, item = null) {
        const modal = document.getElementById('item-modal');
        const title = document.getElementById('modal-title');
        const form = document.getElementById('item-form');

        title.textContent = isEdit ? 'Editar Ítem' : 'Agregar Nuevo Ítem';
        
        if (isEdit && item) {
            // Llenar formulario con datos existentes
            document.getElementById('item-sku').value = item.sku;
            document.getElementById('item-name').value = item.name;
            document.getElementById('item-category').value = item.category;
            document.getElementById('item-location').value = item.location;
            document.getElementById('item-stock').value = item.stock;
            document.getElementById('item-minimum').value = item.minimum;
            document.getElementById('item-price').value = item.price;
            document.getElementById('item-supplier').value = item.supplier;
            document.getElementById('item-description').value = item.description;
            
            form.dataset.editId = item.id;
        } else {
            // Limpiar formulario
            form.reset();
            delete form.dataset.editId;
        }

        modal.classList.add('show');
    }

    showMovementModal(itemId) {
        const item = this.inventory.find(item => item.id === itemId);
        if (!item) return;

        const modal = document.getElementById('movement-modal');
        const form = document.getElementById('movement-form');
        
        form.dataset.itemId = itemId;
        form.reset();
        
        modal.classList.add('show');
    }

    // =======================================================================
    // UTILIDADES
    // =======================================================================

    showNotification(title, message, type = 'info') {
        const notifications = document.getElementById('notifications');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        notification.innerHTML = `
            <div class="notification-header">
                <span class="notification-title">${title}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="notification-message">${message}</div>
        `;
        
        notifications.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    updateUserDisplay() {
        if (this.currentUser) {
            document.getElementById('current-user').textContent = this.currentUser.name;
        }
    }

    populateCategories() {
        const categorySelects = [
            document.getElementById('filter-category'),
            document.getElementById('item-category')
        ];

        categorySelects.forEach(select => {
            if (select) {
                select.innerHTML = '<option value="">Seleccionar categoría</option>';
                this.categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category;
                    option.textContent = category;
                    select.appendChild(option);
                });
            }
        });
    }

    // =======================================================================
    // EXPORTAR/IMPORTAR
    // =======================================================================

    exportData() {
        const data = {
            inventory: this.inventory,
            exportDate: new Date().toISOString(),
            exportedBy: this.currentUser.name
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `inventario_maestranzas_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        this.showNotification('Datos exportados', 'El inventario ha sido exportado correctamente', 'success');
    }

    importData(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                if (data.inventory && Array.isArray(data.inventory)) {
                    this.inventory = data.inventory;
                    this.saveData();
                    this.renderInventory();
                    this.updateStats();
                    this.showNotification('Datos importados', 'El inventario ha sido importado correctamente', 'success');
                } else {
                    throw new Error('Formato de archivo inválido');
                }
            } catch (error) {
                this.showNotification('Error de importación', 'El archivo no es válido', 'error');
            }
        };
        reader.readAsText(file);
    }

    // =======================================================================
    // EVENT LISTENERS
    // =======================================================================

    setupEventListeners() {
        // Login
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (this.login(username, password)) {
                document.getElementById('login-form').reset();
            } else {
                this.showNotification('Error de login', 'Usuario o contraseña incorrectos', 'error');
            }
        });

        // Logout
        document.getElementById('logout-btn').addEventListener('click', () => {
            this.logout();
        });

        // Add item button
        document.getElementById('add-item-btn').addEventListener('click', () => {
            this.showItemModal(false);
        });

        // Item form
        document.getElementById('item-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const itemData = {
                sku: formData.get('sku') || document.getElementById('item-sku').value,
                name: formData.get('name') || document.getElementById('item-name').value,
                category: formData.get('category') || document.getElementById('item-category').value,
                location: formData.get('location') || document.getElementById('item-location').value,
                stock: parseInt(formData.get('stock') || document.getElementById('item-stock').value),
                minimum: parseInt(formData.get('minimum') || document.getElementById('item-minimum').value),
                price: parseFloat(formData.get('price') || document.getElementById('item-price').value),
                supplier: formData.get('supplier') || document.getElementById('item-supplier').value,
                description: formData.get('description') || document.getElementById('item-description').value
            };

            const editId = e.target.dataset.editId;
            if (editId) {
                this.updateItem(parseInt(editId), itemData);
            } else {
                this.addItem(itemData);
            }

            this.closeModal('item-modal');
        });

        // Movement form
        document.getElementById('movement-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const itemId = parseInt(e.target.dataset.itemId);
            const type = document.getElementById('movement-type').value;
            const quantity = parseInt(document.getElementById('movement-quantity').value);
            const reason = document.getElementById('movement-reason').value;

            let finalQuantity = quantity;
            if (type === 'salida') finalQuantity = -quantity;
            else if (type === 'ajuste') {
                const item = this.inventory.find(item => item.id === itemId);
                if (item) {
                    finalQuantity = quantity - item.stock;
                }
            }

            this.adjustStock(itemId, finalQuantity, reason);
            this.closeModal('movement-modal');
        });

        // Search and filter
        document.getElementById('search-input').addEventListener('input', () => {
            this.renderInventory();
        });

        document.getElementById('filter-category').addEventListener('change', () => {
            this.renderInventory();
        });

        // Export/Import
        document.getElementById('export-btn').addEventListener('click', () => {
            this.exportData();
        });

        document.getElementById('import-btn').addEventListener('click', () => {
            document.getElementById('import-modal').classList.add('show');
        });

        // Users Management
        document.getElementById('manage-users-btn').addEventListener('click', () => {
            this.showUsersModal();
        });

        document.getElementById('add-user-btn').addEventListener('click', () => {
            this.showUserFormModal(false);
        });

        // User form
        document.getElementById('user-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const userData = {
                username: document.getElementById('user-username').value.trim(),
                name: document.getElementById('user-name').value.trim(),
                email: document.getElementById('user-email').value.trim(),
                role: document.getElementById('user-role').value,
                password: document.getElementById('user-password').value,
                confirmPassword: document.getElementById('user-confirm-password').value
            };

            const editUsername = e.target.dataset.editUsername;
            if (editUsername) {
                this.updateUser(editUsername, userData);
            } else {
                this.addUser(userData);
            }

            this.closeModal('user-form-modal');
        });

        document.getElementById('import-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const file = document.getElementById('import-file').files[0];
            if (file) {
                this.importData(file);
                this.closeModal('import-modal');
            }
        });

        // Close modals
        document.querySelectorAll('.close-btn, .btn-secondary').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                if (modal) {
                    this.closeModal(modal.id);
                }
            });
        });

        // Close modal on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal.id);
                }
            });
        });
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
            
            // Limpiar formularios al cerrar
            if (modalId === 'user-form-modal') {
                document.getElementById('user-form').reset();
                document.getElementById('user-username').disabled = false;
                document.getElementById('user-password').required = true;
                document.getElementById('user-confirm-password').required = true;
                delete document.getElementById('user-form').dataset.editUsername;
            }
        }
    }

    editItem(id) {
        const item = this.inventory.find(item => item.id === id);
        if (item) {
            this.showItemModal(true, item);
        }
    }

    // =======================================================================
    // GESTIÓN DE USUARIOS
    // =======================================================================

    loadUsers() {
        const savedUsers = localStorage.getItem('users');
        if (savedUsers) {
            this.users = JSON.parse(savedUsers);
        }
    }

    saveUsers() {
        localStorage.setItem('users', JSON.stringify(this.users));
    }

    showUsersModal() {
        this.renderUsers();
        document.getElementById('users-modal').classList.add('show');
    }

    renderUsers() {
        const tbody = document.getElementById('users-tbody');
        tbody.innerHTML = '';

        this.users.forEach(user => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${user.username}</strong></td>
                <td>${user.name}</td>
                <td>${user.email || 'N/A'}</td>
                <td><span class="user-role ${user.role}">${this.getRoleText(user.role)}</span></td>
                <td><span class="user-status active">Activo</span></td>
                <td>
                    <div class="action-buttons">
                        <button class="action-btn btn-primary" onclick="app.editUser('${user.username}')" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn btn-danger" onclick="app.deleteUser('${user.username}')" title="Eliminar" ${user.username === this.currentUser.username ? 'disabled' : ''}>
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    getRoleText(role) {
        const roleTexts = {
            admin: 'Administrador',
            user: 'Usuario',
            almacen: 'Almacén'
        };
        return roleTexts[role] || role;
    }

    showUserFormModal(isEdit = false, user = null) {
        const modal = document.getElementById('user-form-modal');
        const title = document.getElementById('user-modal-title');
        const form = document.getElementById('user-form');

        title.innerHTML = isEdit ? '<i class="fas fa-user-edit"></i> Editar Usuario' : '<i class="fas fa-user-plus"></i> Agregar Usuario';
        
        if (isEdit && user) {
            document.getElementById('user-username').value = user.username;
            document.getElementById('user-name').value = user.name;
            document.getElementById('user-email').value = user.email || '';
            document.getElementById('user-role').value = user.role;
            document.getElementById('user-password').value = '';
            document.getElementById('user-confirm-password').value = '';
            
            // Deshabilitar cambio de username en edición
            document.getElementById('user-username').disabled = true;
            document.getElementById('user-password').required = false;
            document.getElementById('user-confirm-password').required = false;
            
            form.dataset.editUsername = user.username;
        } else {
            form.reset();
            document.getElementById('user-username').disabled = false;
            document.getElementById('user-password').required = true;
            document.getElementById('user-confirm-password').required = true;
            delete form.dataset.editUsername;
        }

        modal.classList.add('show');
    }

    addUser(userData) {
        // Validar que el username no exista
        if (this.users.find(u => u.username === userData.username)) {
            this.showNotification('Error', 'El nombre de usuario ya existe', 'error');
            return false;
        }

        // Validar que las contraseñas coincidan
        if (userData.password !== userData.confirmPassword) {
            this.showNotification('Error', 'Las contraseñas no coinciden', 'error');
            return false;
        }

        const newUser = {
            username: userData.username,
            password: userData.password,
            name: userData.name,
            email: userData.email,
            role: userData.role,
            createdAt: new Date().toISOString()
        };

        this.users.push(newUser);
        this.saveUsers();
        this.renderUsers();
        this.showNotification('Usuario agregado', `${userData.name} ha sido agregado al sistema`, 'success');
        return true;
    }

    updateUser(username, userData) {
        const userIndex = this.users.findIndex(u => u.username === username);
        if (userIndex === -1) return false;

        // Validar contraseñas si se proporcionaron
        if (userData.password && userData.password !== userData.confirmPassword) {
            this.showNotification('Error', 'Las contraseñas no coinciden', 'error');
            return false;
        }

        const updatedUser = {
            ...this.users[userIndex],
            name: userData.name,
            email: userData.email,
            role: userData.role,
            updatedAt: new Date().toISOString()
        };

        // Actualizar contraseña solo si se proporcionó una nueva
        if (userData.password) {
            updatedUser.password = userData.password;
        }

        this.users[userIndex] = updatedUser;
        this.saveUsers();
        this.renderUsers();
        this.showNotification('Usuario actualizado', `${userData.name} ha sido actualizado`, 'success');
        return true;
    }

    deleteUser(username) {
        const user = this.users.find(u => u.username === username);
        if (!user) return false;

        // No permitir eliminar el usuario actual
        if (username === this.currentUser.username) {
            this.showNotification('Error', 'No puedes eliminar tu propio usuario', 'error');
            return false;
        }

        if (confirm(`¿Estás seguro de que deseas eliminar al usuario "${user.name}"?`)) {
            this.users = this.users.filter(u => u.username !== username);
            this.saveUsers();
            this.renderUsers();
            this.showNotification('Usuario eliminado', `${user.name} ha sido eliminado del sistema`, 'success');
            return true;
        }
        return false;
    }

    editUser(username) {
        const user = this.users.find(u => u.username === username);
        if (user) {
            this.showUserFormModal(true, user);
        }
    }

    checkAdminPermissions() {
        if (this.currentUser && this.currentUser.role === 'admin') {
            document.getElementById('manage-users-btn').style.display = 'inline-flex';
        } else {
            document.getElementById('manage-users-btn').style.display = 'none';
        }
    }
}

// Inicializar la aplicación
const app = new InventoryManager(); 