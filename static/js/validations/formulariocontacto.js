
const formulario = document.getElementById('formulariocontacto')
const inputs = document.querySelectorAll('#formulariocontacto input')
const textarea = document.querySelectorAll('#formulariocontacto textarea')

const expresiones = {
	name: /^[a-zA-ZÀ-ÿ\s]{3,40}$/, // Letras y espacios, pueden llevar acentos.
	mensaje: /^[0-9a-zA-ZÀ-ÿ\s]{1,200}$/,
	asunto: /^[a-zA-ZÀ-ÿ\s]{3,40}$/,
	email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
}

	
const campos = {
	name: false,
	asunto:false,
	mensaje: false,
	email: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "name":
			validarCampo(expresiones.name, e.target, 'name');
		break;
		case "email":
			validarCampo(expresiones.email, e.target, 'email');
		break;
		case "asunto":
			validarCampo(expresiones.asunto, e.target, 'asunto');
		break;
	}
}

const validarTextarea = (e) => {
	switch (e.target.name) {
		case "mensaje":
			validarCampoTextarea(expresiones.mensaje, e.target, 'mensaje');
		break;
	}
}


const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.querySelector(`#grupo__${campo} input`).classList.remove('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else {
		document.querySelector(`#grupo__${campo} input`).classList.add('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}	

const validarCampoTextarea = (expresion, textarea, campo) => {
	if(expresion.test(textarea.value)){
		document.querySelector(`#grupo__${campo} textarea`).classList.remove('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else {
		document.querySelector(`#grupo__${campo} textarea`).classList.add('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}



inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});


textarea.forEach((textarea) => {
    textarea.addEventListener('keyup', validarTextarea);
    textarea.addEventListener('blur', validarTextarea);
});

