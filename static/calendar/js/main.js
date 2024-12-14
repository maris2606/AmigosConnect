$(function () {
    // Inicializa o calendário Rome
    rome(inline_cal, { time: false, inputFormat: 'DD / MM / YYYY' }).on('data', function (value) {
        result.value = value; // Atualiza o campo com a data selecionada
    });

    // Função para buscar datas indisponíveis do backend
    function fetchUnavailableDates() {
        // Faz uma requisição AJAX para buscar as datas
        return $.ajax({
            url: '/api/unavailable-dates', // Altere para sua rota no backend
            method: 'GET',
            dataType: 'json',
        });
    }

    // Função para marcar as datas indisponíveis no calendário
    function markUnavailableDates(dates) {
        // Itera sobre cada data indisponível
        dates.forEach(function (date) {
            // Formata a data para 'DD / MM / YYYY'
            const formattedDate = moment(date, 'YYYY-MM-DD').format('DD / MM / YYYY');

            // Procura a célula correspondente no calendário Rome
            $('#inline_cal .day').each(function () {
                const cellDate = $(this).data('date'); // Supondo que cada célula tem um atributo `data-date`

                if (cellDate === formattedDate) {
                    $(this).addClass('indisponivel'); // Adiciona a classe CSS
                }
            });
        });
    }

    // Chama a função para buscar e marcar datas indisponíveis ao carregar a página
    fetchUnavailableDates().then(function (unavailableDates) {
        markUnavailableDates(unavailableDates);
    });

    // Classe CSS para destacar as datas indisponíveis
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            .indisponivel {
                background-color: #f8a900 !important; /* Laranja claro */
                color: white !important;
            }
        `)
        .appendTo('head');
});
