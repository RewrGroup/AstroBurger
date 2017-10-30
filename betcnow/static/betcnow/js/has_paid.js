var ignore_onbeforeunload = false;
var ya_pulsado = false;
history.pushState(null, null, '#');
window.addEventListener('popstate', function(event) {
	history.pushState(null, null, '#');
});
jQuery(function(){
	$('#code-input').on('keyup', function(e){	// Para que cuando se presione enter en lo de canjear codigo, se haga el canje
		if(e.keyCode == 13){
			redeem();
		}
	});
	window.setTimeout(function(){                
		$.ajax({
			url: hp,
			data: {
				'jugadas': numeros_jugadas,
				'pote': pote
			},
			dataType: 'json',
			success: function(data){
				ignore_onbeforeunload = true;
				if (data.paid == false){					
					alert("Your time for paying has expired. Make a new selection!");
					window.location.href = play_url;
				}
			}
		});
	}, 180000);
	window.onunload = window.onbeforeunload = cerrar;
	$(window).unload(cerrar);
	$(window).on('beforeunload pagehide', cerrar);
		function cerrar(){		
		if (ignore_onbeforeunload == false){
			var pago;
		   $.ajax({
				async: false,  //Conexión síncrona porque se necesita esperar que se ejecute la conexión antes de seguir con el método    
				url: hp,
				data: {
					'jugadas': numeros_jugadas,
					'pote': pote
				},
				dataType: 'json',
				success: function(data){
					pago = data.paid;
				}
		   }); 
			if (pago == false){
				return ("you haven't paid yet");
			}
			else{
				ignore_onbeforeunload = true;
			}
		}
	};
});

function jugada_premiada(){
	var title;
	var text;
	var text2="\n";

	$.ajax({
		url: hp,
		data: {
			'jugadas': numeros_jugadas,
			'pote': pote,
			'continue_button': true
		},
		dataType: 'json',
		success: function(data){			
			if (data.paid == true){
				ignore_onbeforeunload = true;
				if (data.lista_premios.length > 0){
					swal({
						html: true,
						title: "Congratulations!",
						text: "You have selected some numbers with gift prizes, and you have won the following gifts!<br><br>" + puntos(data.lista_premios, data.member),
						imageUrl: imgurl
					}, function(){
						window.location.href = play_url;						
					});
				}
				else{
					window.location.href = play_url;
				}
			}
			else{
				swal({
					title: 'Please make your payment before continuing.\n ',
					text: 'If you want to go back, press "Cancel" button'
				});
			}
		}
	}); 				
}

function puntos(lista_premios, member){
	var text = "";
	for(var i=0; i<lista_premios.length; i++){
		text += "<b>" + lista_premios[i];
		if(member == true){
			text += " <span id='x-3'>x3</span>";
		}
		text += "</b><br>";
	}
	return text;
}

function set_popover(content){
	$('#code-button').attr('data-toggle', 'popover');
	$('#code-button').attr('data-content', content);
	$('#code-modal').html("");
	$(function () {
		$('[data-toggle="popover"]').popover();			
	})
}

$(document).ready(function(){	
	if(numeros_jugadas.length > 1){
		set_popover('Codes are only valid for one-number selections');
	}
	else{
		$('#code-button').attr('data-toggle', 'modal');
		$('#code-button').attr('data-target', '#code-modal');
	}
});

function redeem(){
	console.log(1);
	veces_pulsado += 1;
	if (veces_pulsado == 3){
		$('#code-button').attr('disabled', true);
	}
	var codigo = $('#code-input').val();	
	$.ajax({
		url: redeem_url,
		data: {
			'codigo': codigo,
			'numero': numeros_jugadas[0],
			'pote': pote
		},
		dataType: 'json',
		success: function(data){
			$('#code-modal').modal('hide');
			if(data.canjeado == true){
				set_popover('You have already redeemed your code');
				swal({
			  		title: "Code redeemed!",
			  		text: "Your code has been redeemed successfully",
				  	type: "success",
				});
			}
			else{
				swal({
			  		title: "Error",
			  		text: "Invalid or already taken code",
				  	type: "error",
				});
			}
		}
	})
}