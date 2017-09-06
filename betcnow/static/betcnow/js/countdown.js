// Set the date we're counting down to
 //var countDownDate = new Date("2017-06-14 20:00:00.0").getTime();
// Update the count down every 1 second
var countdownfunction = setInterval(function() {	
	if (timer === true){
		// Get todays date and time
		//var now = new Date().getTime();
		now = now + 1000;
		// Find the distance between now an the count down date
		var distance = countDownDate - now;

		// Time calculations for days, hours, minutes and seconds
		var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((distance % (1000 * 60)) / 1000);

		// Output the result in an element with id="demo"
		var ids = ["hours", "minutes", "seconds"];
		var variables = [hours, minutes, seconds];
		for (var i=0; i < 3; i++){
			document.getElementById(ids[i]).innerHTML = "<center><h4 class='numeros-conteo'> " + variables[i] + "</h4></center>";
		}


		// If the count down is over, write some text
		console.log(distance);
		if (distance < 1000) {		
			clearInterval(countdownfunction);
		}
	}
	else{
		clearInterval(countdownfunction);
	}
}, 1000);
