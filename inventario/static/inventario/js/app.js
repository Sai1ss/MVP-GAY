// inventario/static/inventario/js/app.js

// Confirmar antes de borrar un elemento
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a.btn-danger').forEach(el => {
    el.addEventListener('click', e => {
      if(!confirm('¿Seguro que quieres borrar este elemento?')) {
        e.preventDefault();
      }
    });
  });
});

// Aquí puedes añadir más interacciones futuras
// ===== Validación signup =====
document.addEventListener('DOMContentLoaded', () => {
  const pwd1 = document.getElementById('id_password1');
  const pwd2 = document.getElementById('id_password2');
  const submitBtn = document.getElementById('signup-submit');
  const msg = document.getElementById('password-match');

  function checkPasswords() {
    if (pwd1.value && pwd2.value && pwd1.value !== pwd2.value) {
      msg.classList.remove('d-none');
      submitBtn.disabled = true;
    } else {
      msg.classList.add('d-none');
      submitBtn.disabled = false;
    }
  }

  pwd1.addEventListener('input', checkPasswords);
  pwd2.addEventListener('input', checkPasswords);
  checkPasswords(); // inicial
});

// ===== Toggle password visibility =====
document.addEventListener('DOMContentLoaded', () => {
  const pwdInput = document.getElementById('id_password');
  const toggle = document.getElementById('toggle-pwd');
  if (!pwdInput || !toggle) return;

  toggle.addEventListener('click', () => {
    const type = pwdInput.type === 'password' ? 'text' : 'password';
    pwdInput.type = type;
    toggle.textContent = type === 'password' ? 'Mostrar' : 'Ocultar';
  });
});

// === Confirmar cancelar en formulario de elemento ===
document.addEventListener('DOMContentLoaded', () => {
  const cancelBtn = document.getElementById('cancel-btn');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', e => {
      if (!confirm('¿Estás seguro de que deseas cancelar? Se perderán los datos ingresados.')) {
        e.preventDefault();
      }
    });
  }
});

