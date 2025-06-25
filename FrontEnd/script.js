// script.js

const apiUrl = 'http://localhost:5000/usuario'; // ajuste conforme seu backend

// Função para buscar usuários e preencher a tabela
async function carregarUsuarios() {
  const tbody = document.querySelector("#usuarios tbody");
  tbody.innerHTML = "";
  try {
    const response = await fetch(apiUrl);
    const usuarios = await response.json();
    usuarios.forEach(user => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${user.name}</td>
        <td>${user.personality}</td>
        <td><button class="btn btn-danger btn-sm" onclick="deletarUsuario('${user.name}')">
          <i class="bi bi-trash"></i></button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar usuários:", error);
  }
}

// Função para deletar usuário
async function deletarUsuario(nome) {
  if (!confirm(`Deseja realmente deletar ${nome}?`)) return;
  try {
    const response = await fetch(`${apiUrl}/${nome}`, { method: 'DELETE' });
    if (response.ok) {
      await carregarUsuarios();
    } else {
      alert("Erro ao deletar usuário");
    }
  } catch (error) {
    console.error("Erro ao deletar:", error);
  }
}

// Função para enviar formulário
async function enviarFormulario() {
  const form = document.getElementById("formularioPersonalidade");
  const data = {
    name: form.name.value,
    time_spent_alone: parseInt(form.time_spent_alone.value),
    stage_fear: form.stage_fear.value,
    social_event_attendance: parseInt(form.social_event_attendance.value),
    going_outside: parseInt(form.going_outside.value),
    drained_after_socializing: form.drained_after_socializing.value,
    friends_circle_size: parseInt(form.friends_circle_size.value),
    post_frequency: parseInt(form.post_frequency.value)
  };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();

    if (response.ok) {
      Swal.fire({
        icon: 'success',
        title: `Sua personalidade é ${result.personality}`,
        showConfirmButton: false,
        timer: 3000
      });
      form.reset();
      bootstrap.Modal.getInstance(document.getElementById('modalFormulario')).hide();
      await carregarUsuarios();
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Erro ao classificar',
        text: result.message || 'Tente novamente.'
      });
    }
  } catch (error) {
    console.error("Erro no envio:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  carregarUsuarios();
  document.getElementById("abrirModal").addEventListener("click", () => {
    new bootstrap.Modal(document.getElementById('modalFormulario')).show();
  });
  document.getElementById("btnCancelar").addEventListener("click", () => {
    bootstrap.Modal.getInstance(document.getElementById('modalFormulario')).hide();
  });
  document.getElementById("formularioPersonalidade").addEventListener("submit", e => {
    e.preventDefault();
    enviarFormulario();
  });
});
