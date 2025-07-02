// script.js

const apiUrl = 'http://127.0.0.1:5000/usuarios';

// Função para buscar usuários e preencher a tabela
async function carregarUsuarios() {
  const tbody = document.querySelector("#usuarios tbody");
  tbody.innerHTML = "";
  try {
    const response = await fetch(apiUrl);
    const data = await response.json();
    console.log(usuarios)
    data.usuarios.forEach(user => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${user.name}</td>
        <td>${user.personality === "Introvert" ? "Introvertido" : "Extrovertido"}</td>
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
    const response = await fetch(`http://127.0.0.1:5000/usuario?name=${nome}`, { method: 'DELETE' });
    if (response.ok) {
      Swal.fire({
        icon: 'success',        
        title: `Usuário ${nome} deletado com sucesso`,
        showConfirmButton: false,
        timer: 3000
      });
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
    name: form.name.value.trim(),
    time_spent_alone: parseInt(form.time_spent_alone.value),
    stage_fear: form.stage_fear.value,
    social_event_attendance: parseInt(form.social_event_attendance.value),
    going_outside: parseInt(form.going_outside.value),
    drained_after_socializing: form.drained_after_socializing.value,
    friends_circle_size: parseInt(form.friends_circle_size.value),
    post_frequency: parseInt(form.post_frequency.value)
  }; 

  const formData = new FormData();
  for (const key in data) {
  formData.append(key, data[key]); // agora com inteiros reais
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/usuario`, {
      method: 'POST',      
      body: formData
    });
    const result = await response.json();

    if (response.ok) {
      Swal.fire({
        icon: 'success',        
        title: `Sua personalidade é ${result.personality === "Introvert" ? "Introvertido" : "Extrovertido"}`,
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
    new bootstrap.Modal(document.getElementById('modalFormulario'), {
      backdrop: true, 
      keyboard: true,
      focus: true
    }).show();
  });
  document.getElementById("btnCancelar").addEventListener("click", () => {
    bootstrap.Modal.getInstance(document.getElementById('modalFormulario')).hide();
  });
  document.getElementById("formularioPersonalidade").addEventListener("submit", e => {
    e.preventDefault();
    enviarFormulario();
  });
});
