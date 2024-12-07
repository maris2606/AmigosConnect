const mensagem = document.querySelector('#input_mensagem');

const btn = document.querySelector('#btn_enviar');

const chat = document.querySelector('.chat');

chat.scrollTop = chat.scrollHeight;

btn.addEventListener('click', ()=>{
    let msg = mensagem.value;
    
    if (msg.trim() != '') {
        chat.innerHTML += `<div class="enviada p-3 d-flex">
                    <div class="mensagem p-3">
                        <div class="row w-100 m-0">
                            <img class="pfp-pic-msg mr-3" src="/static/icons/Generic avatar.svg" alt="foto de perfil">
                            <p class="user-msg">jossaninha</p>
                        </div>
    
                        <div class="row w-100 m-0 conteudo">
                            <p>${msg}</p>
                        </div>
    
                        <div class="row hora-msg w-100 m-0 d-flex justify-content-end align-items-end">
                            <p class="m-0">16:04</p>
                        </div>
                    </div>
                </div>`
        mensagem.value = '';

        chat.scrollTop = chat.scrollHeight;
    }
});















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


