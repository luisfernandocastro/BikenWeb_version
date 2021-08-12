
const formulario = document.getElementById('formularioeditprofile')
const inputs = document.querySelectorAll('#formularioeditprofile input')

const expresiones = {
    
	telefono: /^\d{7,7}$/, // Letras y espacios, pueden llevar acentos.
	estado: /^[a-zA-ZÀ-ÿ\s]{3,50}$/,
	direccion: /^[a-zA-Z0-9\s\_\#\-]{10,100}$/	
}



	
const campos = {
	estado: false,
    direccion:false,
	telefono: false,
}


const validarFormulario = (e) => {
	switch (e.target.name) {
		case "telefono":
			validarCampo(expresiones.telefono, e.target, 'telefono');
		break;
        case "direccion":
			validarCampo(expresiones.direccion, e.target, 'direccion');
		break;
        case "estado":
			validarCampo(expresiones.estado, e.target, 'estado');
		break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} input`).classList.remove('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} input`).classList.add('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}



inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

