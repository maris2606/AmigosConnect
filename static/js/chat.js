console.log(nome_usuario);

const btn = document.querySelector('#btn_enviar');
const chat = document.querySelector('.chat');

const btn_add_alternativa = document.querySelector('.btn-add-alternativa');
const area_alternativas = document.querySelector('.alternativas-adicionadas');

const btn_cancelar_enquete = document.querySelector('.cancelar-enquete');
const btn_close_enquete = document.querySelector('.close-enquete');

const btn_add_data = document.querySelector('.btn-add-data');

const btn_criar_enquete = document.querySelector('#criar-enquete'); // Botão para criar enquete

btn_add_data.addEventListener("click", () => {
    let selected = document.querySelector('.rd-day-selected');
    if (selected) {
        selected.classList.add('indisponivel');
    }
});

chat.scrollTop = chat.scrollHeight; // Rola para a mensagem mais recente

let n_alt = 2; // Contador de alternativas

// Adicionar alternativa na criação de enquete
btn_add_alternativa.addEventListener('click', () => {
    n_alt++;
    const alternativaHTML = `
    <span class="d-flex justify-content-between w-100">
        <label class="mt-3" for="enquete_a${n_alt}">Alternativa ${n_alt}:</label>
        <input type="text" name="alternativa-${n_alt}" id="enquete_a${n_alt}">
    </span>`;
    area_alternativas.insertAdjacentHTML('beforeend', alternativaHTML);
});

// Função para resetar o formulário de criação de enquete
function resetar_alternativas() {
    n_alt = 2;
    area_alternativas.innerHTML = `
    <span class="d-flex justify-content-between w-100">
        <label class="mt-3" for="enquete_a1">Alternativa 1:</label>
        <input type="text" name="alternativa-1" id="enquete_a1">
    </span>
    <span class="d-flex justify-content-between w-100">
        <label class="mt-3" for="enquete_a2">Alternativa 2:</label>
        <input type="text" name="alternativa-2" id="enquete_a2">
    </span>`;
    document.querySelector('#nome-enquete').value = ''; // Limpa o título da enquete
}

// Reseta o formulário ao cancelar ou fechar a modal
btn_cancelar_enquete.addEventListener('click', resetar_alternativas);
btn_close_enquete.addEventListener('click', resetar_alternativas);

// Objeto de votos para a nova enquete
let votos = {};

// Função para atualizar as barras de progresso
function atualizarBarras() {
    let totalVotos = Object.values(votos).reduce((a, b) => a + b, 0);

    // Atualiza cada barra de acordo com a quantidade de votos
    for (let nome in votos) {
        let porcentagem = totalVotos === 0 ? 0 : (votos[nome] / totalVotos) * 100;
        const barra = document.getElementById(`barra-${nome.toLowerCase().replace(/\s+/g, '-')}`);
        if (barra) {
            barra.style.width = `${porcentagem}%`;
        }
    }
}

// Criação dinâmica da enquete
btn_criar_enquete.addEventListener('click', () => {
    // Captura os dados do formulário de criação
    const titulo = document.querySelector('#nome-enquete').value.trim() || "Enquete";
    const alternativas = [];
    document.querySelectorAll('[id^="enquete_a"]').forEach(input => {
        const valor = input.value.trim();
        if (valor) {
            alternativas.push(valor);
            votos[valor] = 0; // Inicializa os votos para cada alternativa
        }
    });

    if (alternativas.length < 2) {
        alert('Por favor, adicione pelo menos duas alternativas para criar a enquete.');
        return;
    }

    //mandando a enquete para o python
    const enqueteData = {
        titulo: titulo,
        alternativas: alternativas
    };

    // Envia os dados para o Flask via fetch
    fetch('/chat.html', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(enqueteData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Enquete criada com sucesso:', data);
    })
    .catch(error => {
        console.error('Erro ao criar enquete:', error);
    });

    // Gera o HTML da enquete dinamicamente
    const enqueteHTML = `
    <div class="enviada p-3 d-flex">
        <form class="enquete-container" action="" method="post">
            <p class="enquete-titulo">${titulo}</p>
            ${alternativas.map(alt => `
            <div class="opcao">
                <span class="d-flex">
                    <input type="radio" name="opt" class="voto" data-nome="${alt}" id="${alt.toLowerCase().replace(/\s+/g, '-')}">
                    <label class="pl-3" for="${alt.toLowerCase().replace(/\s+/g, '-')}">${alt}</label>
                </span>
                <div class="barra">
                    <div class="barra-preenchida" id="barra-${alt.toLowerCase().replace(/\s+/g, '-')}" style="width: 0%;"></div>
                </div>
            </div>`).join('')}
        </form>
    </div>`;

    // Adiciona a enquete ao chat
    chat.insertAdjacentHTML('beforeend', enqueteHTML);

    // Adiciona eventos de clique para as novas opções de voto
    document.querySelectorAll(".voto").forEach(radio => {
        radio.addEventListener("change", (e) => {
            const nome = e.target.dataset.nome;

            if (e.target.checked) {
                votos[nome]++;
            }

            atualizarBarras();
        });
    });

    // Atualiza a rolagem do chat para mostrar a nova enquete
    chat.scrollTop = chat.scrollHeight;

    // Reseta o formulário
    resetar_alternativas();
});