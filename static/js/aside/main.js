// MUESTRA EL MENU  DE LA BARRA LATERAL
const showMenu = (toggleId, navbarId,bodyId) =>{
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId),
    bodypadding = document.getElementById(bodyId)

    if(toggle && navbar){
        toggle.addEventListener('click', ()=>{
            // APARECER MENU(MUESTRA EÑL MENU COMPLETO)
            navbar.classList.toggle('shownav')
            // ROTATE TOGGLE(ICONO DE CONTRAER BARRA LATERAL) GIRA 180°
            toggle.classList.toggle('rotate')
            // PADDING BODY,EL BODY MINIMIZA EL PADDING IZQUIERDO PARA QUE LA BARRA NO TAPE PARTE DE ESTE
            bodypadding.classList.toggle('expander')
        })
    }
}
showMenu('nav-toggle','navbar','body')





