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

    setTimeout(function () {
        // Seleciona o contêiner do calendário e exibe o HTML
        console.log($('.rd-container').html()); // Mudado para selecionar o contêiner correto
    }, 500); // Aguarda 500ms para garantir que o calendário foi renderizado

    // Função para marcar as datas indisponíveis no calendário
    function markUnavailableDates(dates) {
        // Itera sobre cada data indisponível
        dates.forEach(function (date) {
            // Formata a data para 'DD / MM / YYYY'
            const formattedDate = moment(date, 'YYYY-MM-DD').format('DD/MM/YYYY').trim(); // Remove espaços
            console.log('Data formatada para verificação:', formattedDate);  // Log para debug

            console.log($('.rd-container .rd-day-body').length);  // Verifica quantos elementos .rd-day-body foram encontrados
            $('.rd-container .rd-day-body').each(function () {
                const cellDay = $(this).text().trim(); // Pega o texto da célula de data (dia)
                console.log('Dia da célula:', cellDay);

                // Pega o mês e o ano do cabeçalho
                const monthYear = $('.rd-container .rd-month-label').text().trim(); // Exemplo: "December 2024"
                const [month, year] = monthYear.split(' ');

                // Converte o nome do mês para o número do mês (01, 02, ..., 12)
                const monthNumber = getMonthNumber(month);

                // Monta a data completa no formato 'DD/MM/YYYY'
                const fullDate = `${cellDay.padStart(2, '0')}/${monthNumber}/${year}`;

                console.log('Data completa da célula:', fullDate);
                console.log('Data selecionada: ', formattedDate); // Corrigido para fechar o parêntese

                // Verifica se a célula de data corresponde à data formatada
                if (fullDate === formattedDate) {
                    $(this).addClass('indisponivel'); // Adiciona a classe "indisponivel" à célula correspondente
                } else {
                    console.log('Datas diferentes');
                }
            });
        }); // Fecha o forEach
    } // Fecha a função markUnavailableDates

    // Chama a função para buscar e marcar datas indisponíveis ao carregar a página
    fetchUnavailableDates().then(function (unavailableDates) {
        markUnavailableDates(unavailableDates); // Marca as datas indisponíveis
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
}); // Fecha o $(function)


// Função para converter o nome do mês para o número do mês
function getMonthNumber(monthName) {
    const months = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    };

    return months[monthName] || '01'; // Retorna o número do mês ou '01' se não encontrar
} // Fecha a função getMonthNumber
