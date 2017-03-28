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
	var text3 = "\nKeep your membership on date, so you can keep earning these and many more amazing gifts!\n";

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
					if (data.member == true){
						title = "Congratulations!";	
						text = "You have selected some numbers with gift prizes, and you have won the following gifts!:\n\n";
					}
					else{
						title = "Congrat... Oh Wait!";
						text = "You have selected some numbers with gift prizes! you could have won these gifts:\n\n";
						text2 = "\n\nBut since you haven't upgraded your membership yet, we can't give you those gifts :(\n";
					}
					swal({
						title: title,
						text: text + (data.lista_premios) + text2 + text3,						
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