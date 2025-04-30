document.addEventListener('DOMContentLoaded', () => {
  fetch('http://localhost:4000/cars') // <- ajuste aqui, porta 4000 ou a usada no backend
    .then(response => response.json())
    .then(data => {
      const lista = document.getElementById('lista-veiculos');
      lista.innerHTML = '';

      data.forEach(veiculo => {
        const item = document.createElement('li');
        item.textContent = `${veiculo.modelo} (${veiculo.anoVeiculo}) - ${veiculo.placa}`;
        lista.appendChild(item);
      });
    })
    .catch(error => {
      console.error('Erro ao buscar veículos:', error);
    });
});

