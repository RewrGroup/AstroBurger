var ignore_onbeforeunload = false;
var ya_pulsado = false;

history.pushState(null, null, '#');
window.addEventListener('popstate', function(event) {
	history.pushState(null, null, '#');
});
jQuery(function(){            	
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
	window.onbeforeunload = function(){
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
	if (ya_pulsado == false){
		$.ajax({
			url: hp,
			data: {
				'jugadas': numeros_jugadas,
				'pote': pote
			},
			dataType: 'json',
			success: function(data){
				ya_pulsado = true;
				if (data.paid == true){
					ignore_onbeforeunload = true;
					if (data.lista_premios.length > 0){
						swal({
							title: "Congratulations!", 
							text: "You have won the following gifts: " + (data.lista_premios),							
							imageUrl: "static/betcnow/img/gift-flat.png"
						}, function(){
							window.location.href = play_url;
						});						
					}
					else{
						window.location.href = play_url;
					}
				}
			}
		}); 		
	}	
}