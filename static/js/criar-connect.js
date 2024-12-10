const amgs_selecionados = document.querySelector('.amigos-selecionados');
const amgs_select = document.querySelector('#amigos_select');
const btn_cancelar = document.querySelector('.cancelar');

// Escuta a mudança na seleção
amgs_select.addEventListener('change', (e) => {
    const selecionado = e.target.value;

    if (selecionado != '0') {
        console.log(amgs_selecionados);

        // Adiciona o amigo à lista de amigos selecionados, se ainda não estiver na lista
        if (!amgs_selecionados.innerHTML.includes(`<div class="amg d-flex justify-content-around align-items-center"> <p class='m-0 p-0'>${selecionado}</p> <a src="#" class="remove-amg"><img src="/static/icons/close.svg" class="icon-btn" alt="ícone de saída"></a> </div>`)) {
            amgs_selecionados.innerHTML += `<div class="amg d-flex justify-content-around align-items-center"> <p class='m-0 p-0'>${selecionado}</p> <a src="#" class="remove-amg"><img src="/static/icons/close.svg" class="icon-btn" alt="ícone de saída"></a> </div>`;
        }
    }

    // Adiciona o evento de remoção do amigo da lista
    document.querySelectorAll('.remove-amg').forEach((b) => {
        b.addEventListener('click', (e) => {
            e.target.parentElement.parentElement.remove();
        });
    });

    // Atualiza o valor do campo oculto com os amigos selecionados
    const amigosSelecionadosArray = Array.from(amgs_selecionados.children)
                                         .map(child => child.querySelector('p').textContent.trim());
    document.getElementById('amigos_selecionados_input').value = amigosSelecionadosArray.join(',');
});

// Cancelar ação (não salva nada, apenas redireciona)
btn_cancelar.addEventListener('click', () => {
    window.location.href = '/templates/feed.html';
});
