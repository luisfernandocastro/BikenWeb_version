from django.core.validators import RegexValidator # validaciones de los inputs de los formularios 


# vaidaciones de datos de los campos(inputs)
validatorLetters= RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El campo de marca solo puede contener letras")
validatornumdocumento = RegexValidator(r"^\d{8,10}$","Ingrese un numero de documento válido")


validatorEstado = RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","Agregue solo letras en el campo de estado")
validatorFirst_name = RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El nombre no puede contener números, ni caracteres especiales")
validatorLast_name = RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El Apellido no puede contener números, ni caracteres especiales")
validatornumcelular = RegexValidator(r"^\d{10,10}$","Inserte un número de celular válido")
validatornumtelefono =  RegexValidator(r"^\d{7,7}$","Inserte un número de teléfono válido")
validatordireccion = RegexValidator(r"^[a-zA-Z0-9\s\_\#\-]{10,100}$", "Inserte una dirección válida") 
validatortextarea = RegexValidator(r"^[0-9a-zA-ZÀ-ÿ\s]{1,200}$", "Este campo no acepta caracteres especiales")
validatorname= RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El campo de nombres y apellidos solo puede contener letras")
validatorasunto= RegexValidator(r"^[a-zA-ZÀ-ÿ\s]{1,40}$","El campo de asunto solo puede contener letras")