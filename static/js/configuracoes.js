const btn_modo = document.querySelector('.btn-modo');
const img_modo = document.querySelector('.btn-modo img');
const p_modo = document.querySelector('.btn-modo p');

btn_modo.addEventListener('click', (e)=>{

    if (e.target.classList.contains('btn-modo-claro')){

        btn_modo.classList.remove('btn-modo-claro');
        btn_modo.classList.add('btn-modo-escuro');
    
        img_modo.setAttribute('src', '/static/icons/dark_mode_w.svg');
    
        p_modo.innerHTML = 'escuro';
    } else {

        btn_modo.classList.remove('btn-modo-escuro');
        btn_modo.classList.add('btn-modo-claro');
    
        img_modo.setAttribute('src', '/static/icons/modo_claro.svg');
    
        p_modo.innerHTML = 'claro';
    }
});


