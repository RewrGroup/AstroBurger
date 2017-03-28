jQuery(function(){
	$(window).scroll(function() {
	   var hT = $('#animation-igniter').offset().top,
		   hH = $('#animation-igniter').outerHeight(),
		   wH = $(window).height(),
		   wS = $(this).scrollTop();
	   if (wS > (hT+hH-wH)){
		  $('#step-1').addClass('en-pantalla');
	   } else {
		  $('#step-1').removeClass('en-pantalla');
	   }
	});
	$(window).scroll(function() {
	   var hT = $('#animation-igniter-2').offset().top,
		   hH = $('#animation-igniter-2').outerHeight(),
		   wH = $(window).height(),
		   wS = $(this).scrollTop();
	   if (wS > (hT+hH-wH)){
		  $('#step-2').addClass('en-pantalla-2');
	   } else {
		  $('#step-2').removeClass('en-pantalla-2');
	   }
	});
	$(window).scroll(function() {
	   var hT = $('#animation-igniter-3').offset().top,
		   hH = $('#animation-igniter-3').outerHeight(),
		   wH = $(window).height(),
		   wS = $(this).scrollTop();
	   if (wS > (hT+hH-wH)){
		  $('#step-3').addClass('en-pantalla');
	   } else {
		  $('#step-3').removeClass('en-pantalla');
	   }
	});
	$(window).scroll(function() {
	   var hT = $('#animation-igniter-4').offset().top,
		   hH = $('#animation-igniter-4').outerHeight(),
		   wH = $(window).height(),
		   wS = $(this).scrollTop();
	   if (wS > (hT+hH-wH)){
		  $('#step-4').addClass('en-pantalla-2');
	   } else {
		  $('#step-4').removeClass('en-pantalla-2');
	   }
	});
	
	$(window).scroll(function() {
	   var hT = $('.iconos-countdown').offset().top,
		   hH = $('.iconos-countdown').outerHeight(),
		   lmT = $('#icono-candado').offset().top,
		   lmH = $('#icono-candado').outerHeight(),
		   wH = $(window).height(),
		   wS = $(this).scrollTop();
	   if ((wS > (hT+hH-wH) && (hT > wS) && (wS+wH > hT+hH)) || (wS > (lmT+lmH-wH) && (lmT > wS) && (wS+wH > lmT+lmH))){
		  $('.iconos-countdown').addClass('iconos-countdown-claros');
	   } else {
		  $('.iconos-countdown').removeClass('iconos-countdown-claros');
	   }
	});
});