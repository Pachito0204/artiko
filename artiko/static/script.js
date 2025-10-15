document.getElementById('year').textContent = new Date().getFullYear();

const form = document.getElementById('contactForm');
const status = document.getElementById('formStatus');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  status.textContent = 'Enviando...';
  const data = {
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    phone: form.phone.value.trim(),
    company: form.company.value.trim(),
    message: form.message.value.trim()
  };

  try{
    const res = await fetch('/contact', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    const j = await res.json();
    if(res.ok){
      status.textContent = 'Gracias — tu mensaje fue enviado.';
      form.reset();
    } else {
      status.textContent = j.error || 'Ocurrió un error al enviar.';
    }
  }catch(err){
    status.textContent = 'No se pudo conectar con el servidor.';
  }
});