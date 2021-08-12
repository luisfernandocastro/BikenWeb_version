
const formulario = document.getElementById('formulariochangepassword')
const inputs = document.querySelectorAll('#formulariochangepassword input')

const expresiones = {
	// username: /^[a-zA-Z0-9\_\-\@\.\+]{4,16}$/, // Letras, numeros, guion y guion_bajo
	// first_name: /^[a-zA-ZÀ-ÿ\s]{3,40}$/, // Letras y espacios, pueden llevar acentos.
	// last_name: /^[a-zA-ZÀ-ÿ\s]{3,40}$/, // Letras y espacios, pueden llevar acentos.
	// numcelular: /^\d{10,10}$/, // 7 a 10 numeros.
	// email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	new_password1: /^.{8,100}$/ // 8 a 12 digitos.
}

	
const campos = {
	// username: false,
	// first_name: false,
	// last_name: false,
	// numcelular: false,
	// email: false,
	new_password1: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "new_password1":
			validarCampo(expresiones.new_password1, e.target, 'new_password1');
			validarPassword2();
		break;
		case "new_password2":
			validarPassword2();
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



const validarPassword2 = () => {
	const inputPassword1 = document.getElementById('new_password1');
	const inputPassword2 = document.getElementById('new_password2');

	if(inputPassword1.value !== inputPassword2.value || inputPassword2.value == ""){
		document.getElementById(`grupo__new_password2`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__new_password2`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__new_password2 input`).classList.add('input__error');
		document.querySelector(`#grupo__new_password2 .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos['password'] = false;
	} else {
		document.getElementById(`grupo__new_password2`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__new_password2`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__new_password2 input`).classList.remove('input__error');	
		document.querySelector(`#grupo__new_password2 .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos['password'] = true;
	}
}


inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

