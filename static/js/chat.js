const mensagem = document.querySelector('#input_mensagem');

const btn = document.querySelector('#btn_enviar');

const chat = document.querySelector('.chat');

const btn_add_alternativa = document.querySelector('.btn-add-alternativa');

const area_alternativas = document.querySelector('.alternativas-adicionadas');

const btn_cancelar_enquete =  document.querySelector('.cancelar-enquete');
const btn_close_enquete =  document.querySelector('.close-enquete');

// rola pra mensagem mais recente
chat.scrollTop = chat.scrollHeight;

// provavelmente aqui nessa função viria algo semelhante pra enviar midia. mas a gnt pensa dps.
// evento de enviar mensagem pro chat
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


let n_alt = 2;

// adicionar alternativa na criação de enquete
btn_add_alternativa.addEventListener('click', ()=>{

    // a cada alternativa adiciona um pro id ser diferente
    n_alt++;

    area_alternativas.innerHTML += `
    <span class="d-flex justify-content-between w-100">
        <label class="mt-3" for="enquete_a${n_alt}">Alternativa ${n_alt}:</label>
        <input type="text" name="alternativa-${n_alt}" id="enquete_a${n_alt}">
    </span>
    ` ;
});


function resetar_alternativas () {
    area_alternativas.innerHTML = `<span class="d-flex justify-content-between w-100">
        <label class="mt-3" for="enquete_a1">Alternativa 1:</label>
        <input type="text" name="alternativa-1" id="enquete_a1">
    </span>

    <span class="d-flex justify-content-between w-100">
        <label class="mt-3" for="enquete_a2">Alternativa 2:</label>
        <input type="text" name="alternativa-2" id="enquete_a2">
    </span>`;
}

btn_cancelar_enquete.addEventListener('click', ()=>{
    resetar_alternativas();
});

// precisa ter os dois pq a pessoa pode fechar pelo x
btn_close_enquete.addEventListener('click', ()=>{
    resetar_alternativas();
});









// esse daqui o chat ajudou, mas funcionou direitinho e a logica ta ok

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


