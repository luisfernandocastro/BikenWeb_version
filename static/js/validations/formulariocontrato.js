
const formulario = document.getElementById('formulariocontrato')
const inputs = document.querySelectorAll('#formulariocontrato input')

const expresiones = {

    direccion: /^[a-zA-Z0-9\s\_\#\-]{10,100}$/,
	numerodocumento: /^\d{8,10}$/, // 7 a 10 numeros.
	horainicio:  /^(0[0-9]|1[0-9]|2[0-3]|[0-9]):[0-5][0-9]$/
}

	
const campos = {
    direccion: false,
	numerodocumento: false,
	horainicio: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "direccion":
			validarCampo(expresiones.direccion, e.target, 'direccion');
		break;
		case "numerodocumento":
			validarCampo(expresiones.numerodocumento, e.target, 'numerodocumento');
		break;
		case "horainicio":
			validarCampo(expresiones.horainicio, e.target, 'horainicio');
		break;
		case "horafin":
			validarhora();
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

	// if(campos.direccion && campos.numerodocumento ){

	// 	document.getElementById('buttonsubmit').classList.remove('ocultarboton');	
	// } else {
	// 	document.getElementById('buttonsubmit').classList.add('ocultarboton');
	
	// }
}



const validarhora = () => {
	const horainicio = document.getElementById('horainicio');
	const horafin = document.getElementById('horafin');

	if(horainicio.value == horafin.value){
		document.getElementById(`grupo__horafin`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__horafin`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__horafin input`).classList.add('input__error');
		document.querySelector(`#grupo__horafin .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos['horainicio'] = false;
	} else {
		document.getElementById(`grupo__horafin`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__horafin`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__horafin input`).classList.remove('input__error');	
		document.querySelector(`#grupo__horafin .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos['horainicio'] = true;
	}
}



inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});



