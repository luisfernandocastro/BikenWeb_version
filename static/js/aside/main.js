// SHOW MENU
const showMenu = (toggleId, navbarId,bodyId) =>{
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId),
    bodypadding = document.getElementById(bodyId)

    if(toggle && navbar){
        toggle.addEventListener('click', ()=>{
            // APARECER MENU
            navbar.classList.toggle('show')
            // ROTATE TOGGLE
            toggle.classList.toggle('rotate')
            // PADDING BODY
            bodypadding.classList.toggle('expander')
        })
    }
}
showMenu('nav-toggle','navbar','body')



// const showMenu = (togglesearchId, navbarsearchId,bodysearchId) =>{
//     const togglesearch = document.getElementById(togglesearchId),
//     navbarsearch = document.getElementById(navbarsearchId),
//     bodypaddingsearch = document.getElementById(bodysearchId)

//     if(togglesearch && navbarsearch){
//         toggle.addEventListener('click', ()=>{
//             // APARECER MENU
//             navbarsearch.classList.toggle('show')
//             // ROTATE TOGGLE
//             // toggle.classList.toggle('rotate')
//             // PADDING BODY
//             bodypaddingsearch.classList.toggle('expander')
//         })
//     }
// }
// showMenu('nav-toggle_search','navbar','body')



