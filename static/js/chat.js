

// Inicializa um objeto de votos para armazenar os votos de cada opção
let votos = {
    "Bienal do Livro": 5,
    "Ibirapuera": 7,
    "Paulista": 6,
    "Tucuruvi": 10
};

// Função para atualizar as barras de progresso
function atualizarBarras() {
    let totalVotos = Object.values(votos).reduce((a, b) => a + b, 0);

    // Atualiza cada barra de acordo com a quantidade de votos
    for (let nome in votos) {
        let porcentagem = totalVotos === 0 ? 0 : (votos[nome] / totalVotos) * 100;
        const barra = document.getElementById(`barra-${nome.toLowerCase().replace(/\s+/g, '-')}`);
        barra.style.width = `${porcentagem}%`;
    }
}


// Adiciona evento de 'click' para todos os radio
document.querySelectorAll(".voto").forEach(radio => {
    radio.addEventListener("change", (e) => {
        const nome = e.target.dataset.nome;
    
        // Verifica se a opção foi marcada ou desmarcada
        if (e.target.checked) {
            votos[nome]++;
        } else {
            votos[nome]--;
        }
    
        // Atualiza as barras
        atualizarBarras();
    });

});

// Chama a função para inicializar as barras
atualizarBarras();
