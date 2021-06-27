//------------efecto de carga de las paginas---------------------
$(window).on('load', function () {
	setTimeout(function () {
		$(".loader-page").css({ visibility: "hidden", opacity: "0" })
	}, 2000);
});


//--------agrega un color de fondo a todos los inputs---------------
// $(document).ready(function () {
// 	$("input").focus(function () {
// 		$(this).css("background-color", "#F1F5FC");
// 	});
// 	$("input").blur(function () {
// 		$(this).css("background-color", "white");
// 	});
// }); html:





// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function () {
	var fileName = $(this).val().split("\\").pop();
	$(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});



$(document).ready(function () {
	$('[data-toggle="tooltip"]').tooltip();
});





$(document).ready(function () {
	$("#myInput").on("keyup", function () {
		var value = $(this).val().toLowerCase();
		$("#myTable tr").filter(function () {
			$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
		});
	});
});



// ------------------- Funciones para el modo nocturno----------------


const btnswitch = document.querySelector('#switch');

btnswitch.addEventListener('click', () => {
	document.body.classList.toggle('dark');
	btnswitch.classList.toggle('active');

	// Guardar el modo nocturno en Storage
	if (document.body.classList.contains('dark')) {
		localStorage.setItem('dark-mode', 'true');
	} else {
		localStorage.setItem('dark-mode', 'false');
	}
});

// Obtenemos el modo de estilo actual
if (localStorage.getItem('dark-mode') === 'true') {
	document.body.classList.add('dark');
	btnswitch.classList.add('active');
}else{
	document.body.classList.remove('dark');
	btnswitch.classList.remove('active');

}


document.getElementById('switch').addEventListener('click', function () {
	var icon = document.getElementById('icon');
	icon.classList.toggle('fa-sun');
	icon.classList.toggle('fa-moon');
})





// -------------------end funciones para modo nocturno--------