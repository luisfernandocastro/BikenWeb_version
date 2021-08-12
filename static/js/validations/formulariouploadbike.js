
const formulario = document.getElementById('formulariouploadbike')
const inputs = document.querySelectorAll('#formulariouploadbike input')
const textarea = document.querySelectorAll('#formulariouploadbike textarea')

const expresiones = {
	marca: /^[a-zA-ZÀ-ÿ\s]{3,40}$/, // Letras y espacios, pueden llevar acentos.
	descripcionbici: /^[a-zA-ZÀ-ÿ\s]{1,40}$/,
	precioalquiler: /^[0-9]+([.][0-9]+)?$/
}

	
const campos = {
	marca: false,
	descripcionbici: false,
	precioalquiler: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "marca":
			validarCampo(expresiones.marca, e.target, 'marca');
		break;
		case "precioalquiler":
			validarCampo(expresiones.precioalquiler, e.target, 'precioalquiler');
		break;
	}
}

const validartextarea = (e) =>{
	switch (e.target.name){
		case "descripcionbici":
			validarTextarea(expresiones.descripcionbici, e.target, 'descripcionbici');
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

const validarTextarea = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} textarea`).classList.remove('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} textarea`).classList.add('input__error');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}



inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

textarea.forEach((textarea) =>{
	textarea.addEventListener('Keyup',validartextarea);
	textarea.addEventListener('blur',validartextarea);
});
