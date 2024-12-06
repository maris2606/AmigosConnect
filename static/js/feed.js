

document.querySelectorAll(".heart-button").forEach((btn)=>{
    btn.addEventListener('click', (e)=>{

        const img = e.currentTarget.querySelector("img");

        if (img){
            mudar_icon(img);
        }
    });
});


function mudar_icon(img){
    if (img.classList.contains("heart-button-v")){

        img.classList.remove("heart-button-v");
        img.classList.add("heart-button-p");
        img.setAttribute('src', '/static/icons/heart_filled.svg');
    } else {
        img.classList.remove("heart-button-p");
        img.classList.add("heart-button-v");
        img.setAttribute('src', '/static/icons/heart.svg');
    }
}

document.querySelector('.close').addEventListener('click', ()=>{
    const inputs = document.querySelectorAll('input');

    inputs.forEach((i)=>{
        i.value = '';
    });
});


document.querySelector('.cancelar').addEventListener('click', ()=>{
    const inputs = document.querySelectorAll('input');

    inputs.forEach((i)=>{
        i.value = '';
    });
});



