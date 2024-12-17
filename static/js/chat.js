console.log(nome_usuario);
console.log('o usuário é: ', usuario_logado);
const btn = document.querySelector('#btn_enviar');
const chat = document.querySelector('.chat');

const btn_add_alternativa = document.querySelector('.btn-add-alternativa');
const area_alternativas = document.querySelector('.alternativas-adicionadas');

const btn_cancelar_enquete = document.querySelector('.cancelar-enquete');
const btn_close_enquete = document.querySelector('.close-enquete');

const btn_add_data = document.querySelector('.btn-add-data');

const btn_criar_enquete = document.querySelector('#criar-enquete'); 

let votos = {}; // Objeto de votos, agora será por enquete

// Função para atualizar as barras de progresso
function atualizarBarras(enqueteId) {
    let totalVotos = Object.values(votos[enqueteId]).reduce((a, b) => a + b, 0);

    // Atualiza cada barra de acordo com a quantidade de votos
    for (let nome in votos[enqueteId]) {
        let porcentagem = totalVotos === 0 ? 0 : (votos[enqueteId][nome] / totalVotos) * 100;
        const barra = document.getElementById(`barra-${nome.toLowerCase().replace(/\s+/g, '-')}`);
        if (barra) {
            barra.style.width = `${porcentagem}%`;
        }
    }
}

// Função para renderizar enquetes criadas do banco de dados
function renderizarEnquetes(enquetes) {
    console.log('dentro de renderizar enquetes');
    enquetes.forEach(enquete => {
        let enqueteHTML = ''; // Inicializa a variável para armazenar o HTML da enquete

        console.log('id do usuário da enquete ', enquete.idUsuario);
        if (enquete.idUsuario == usuario_logado) {
            enqueteHTML = `<div class="enviada p-3 d-flex">`;  // Classe "enviada" para enquetes do usuário logado
        } else {
            enqueteHTML = `<div class="recebida p-3 d-flex">`; // Classe "recebida" para enquetes de outros usuários
        }

        // Certifique-se de que o ID da enquete esteja sendo capturado corretamente
        const idEnquete = enquete.idEnquete; // Agora estamos acessando o id da enquete corretamente

        // Adiciona a enquete ao objeto de votos
        votos[idEnquete] = {};  

        // Inicializa os votos para as opções dessa enquete
        enquete.opcoes.forEach(opcao => {
            votos[idEnquete][opcao.textoOpcao] = 0;  // Inicializa o contador de votos para cada alternativa
        });

        // Adiciona o título e as opções de voto da enquete
        enqueteHTML += `
            <form class="enquete-container" action="" method="post">
                <p class="enquete-titulo">${enquete.nomeEnquete}</p>
                ${enquete.opcoes.map(opcao => `
                    <div class="opcao">
                        <span class="d-flex">
                            <input type="radio" name="opt-${idEnquete}" class="voto" data-nome="${opcao.textoOpcao}" data-enquete-id="${idEnquete}" id="${opcao.idOpcao}" />
                            <label class="pl-3" for="opt-${opcao.textoOpcao.toLowerCase().replace(/\s+/g, '-')}" >${opcao.textoOpcao}</label>
                        </span>
                        <div class="barra">
                            <div class="barra-preenchida" id="barra-${opcao.idOpcao}" style="width: 0%;"></div>
                        </div>
                    </div>`).join('')}
            </form>
        </div>`;

        // Adiciona a enquete ao chat
        chat.insertAdjacentHTML('beforeend', enqueteHTML);

        // Adiciona eventos para atualizar os votos e as barras
        document.querySelectorAll(`.voto[data-enquete-id="${idEnquete}"]`).forEach(radio => {
            radio.addEventListener("change", (e) => {
                const nome = e.target.dataset.nome;
                const idEnquete = e.target.dataset.enqueteId;
                const idOpcao = e.target.id;  // ID da opção selecionada

                if (e.target.checked) {
                    votos[idEnquete][nome]++;
                }

                // Atualiza as barras para essa enquete
                atualizarBarras(idEnquete);

                // Envia os votos para o servidor, incluindo o ID da opção selecionada
                enviarVotos(idEnquete, idOpcao);
            });
        });
    });

    // Atualiza a rolagem do chat para mostrar as enquetes renderizadas
    chat.scrollTop = chat.scrollHeight;
}

// Função para enviar os votos ao servidor
function enviarVotos(idEnquete, idOpcao) {
    // Garantir que votosData esteja preenchido corretamente
 
    console.log('Enviando dados de votos:', idEnquete, idOpcao); // Verifique se está correto

    fetch('/chat.html', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ idEnquete: idEnquete, idOpcaoAlterada: idOpcao }) // Envia os dados como JSON
    })
    .then(response => {
        // Verifica se a resposta é JSON antes de tentar analisá-la
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Erro na resposta do servidor: ' + response.statusText);
        }
    })
    .then(data => {
        console.log('Votos enviados com sucesso:', data);
    })
    .catch(error => {
        console.error('Erro ao enviar votos:', error);
    });
}


// Renderizar enquetes puxadas do banco de dados
renderizarEnquetes(enquetes);

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

// Adicionar alternativa na criação de enquete
let n_alt = 2; // Contador de alternativas
btn_add_alternativa.addEventListener('click', () => {
    n_alt++;
    const alternativaHTML = `
    <span class="d-flex justify-content-between w-100">
        <label class="mt-3" for="enquete_a${n_alt}">Alternativa ${n_alt}:</label>
        <input type="text" name="alternativa-${n_alt}" id="enquete_a${n_alt}">
    </span>`;
    area_alternativas.insertAdjacentHTML('beforeend', alternativaHTML);
});

// Criação dinâmica da enquete
btn_criar_enquete.addEventListener('click', () => {
    // Captura os dados do formulário de criação
    const titulo = document.querySelector('#nome-enquete').value.trim() || "Enquete";
    const alternativas = [];
    const idEnquete = Date.now();  // Gerando um ID único para a enquete

    document.querySelectorAll('[id^="enquete_a"]').forEach(input => {
        const valor = input.value.trim();
        if (valor) {
            alternativas.push(valor);
            votos[idEnquete] = votos[idEnquete] || {};  // Inicializa a estrutura de votos para esta enquete
            votos[idEnquete][valor] = 0;  // Inicializa o contador de votos
        }
    });

    // Envia os dados para o Flask via fetch
    const enqueteData = {
        idEnquete: idEnquete, // Certifique-se de que está usando o idEnquete gerado
        titulo: titulo,
        alternativas: alternativas
    };

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
                    <input type="radio" name="opt-${idEnquete}" class="voto" data-nome="${alt}" data-enquete-id="${idEnquete}" id="opt-${alt.toLowerCase().replace(/\s+/g, '-')}" />
                    <label class="pl-3" for="opt-${alt.toLowerCase().replace(/\s+/g, '-')}" >${alt}</label>
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
    document.querySelectorAll(`.voto[data-enquete-id="${idEnquete}"]`).forEach(radio => {
        radio.addEventListener("change", (e) => {
            const nome = e.target.dataset.nome;
            const idEnquete = e.target.dataset.enqueteId;
            const idOpcao = e.target.id;  // ID da opção selecionada

            if (e.target.checked) {
                votos[idEnquete][nome]++;  // Atualiza o voto para essa opção
            }

            atualizarBarras(idEnquete);
            enviarVotos(idEnquete, idOpcao);
        });
    });

    // Atualiza a rolagem do chat para mostrar a nova enquete
    chat.scrollTop = chat.scrollHeight;

    // Reseta o formulário
    resetar_alternativas();
});
