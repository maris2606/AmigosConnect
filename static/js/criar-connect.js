
const amgs_selecionados = document.querySelector('.amigos-selecionados');

const amgs_select = document.querySelector('#amigos_select');



amgs_select.addEventListener('change',(e)=>{
    const selecionado = e.target.value;

    if (selecionado != '0'){
        console.log(amgs_selecionados);
        

        if (!amgs_selecionados.innerHTML.includes(`<div class="amg d-flex justify-content-around align-items-center"> <p class='m-0 p-0'>${selecionado}</p> <a src="#" class="remove-amg"><img src="/static/icons/close.svg" class="icon-btn" alt="ícone de saída"></a> </div>`)){
            
            amgs_selecionados.innerHTML +=`<div class="amg d-flex justify-content-around align-items-center"> <p class='m-0 p-0'>${selecionado}</p> <a src="#" class="remove-amg"><img src="/static/icons/close.svg" class="icon-btn" alt="ícone de saída"></a> </div>`;
        
        }
    }
    
    document.querySelectorAll('.remove-amg').forEach((b)=>{

        b.addEventListener('click', (e)=> {
            e.target.parentElement.parentElement.remove();
            
        });
    });
});


