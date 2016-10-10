// Tools Panel

jQuery(function($j) {
	
    "use strict";
	
	// ini toggles on load
	if ($j('header').hasClass("header--sticky")) {
		 $j('#tglFloatHeader').addClass("checked");
	}
	if ($j('body').hasClass("boxed")) {
		 $j('#tglBoxed').attr('checked', 'checked');
	}	
	if ($j('body').hasClass("fullwidth")) {
		 $j('#tglFull').attr('checked', 'checked');
	}	
	if ($j('body').hasClass("wide")) {
		 $j('#tglWide').attr('checked', 'checked');
	}		
   $j('.menu-btn').click(function() {
      $j('.box-out').toggleClass('box-in');
	  $j('.box-out .icon').toggleClass('rotating');
    });

   $j('#tglFloatHeader').click(function() {
      $j(this).toggleClass("checked");
	  $j('header').toggleClass("header--sticky");
    });	
	
   $j('#tglBoxed').click(function() { 
	  $j('body').removeClass("fullwidth");
	  setTimeout(function() {
		$j('header .navbar').addClass('stuck--smaller');
	  }, 300);
	  $j('body').removeClass("wide");
	  $j('body').addClass("boxed");
	  $j('.slick-initialized').slick('setPosition');
	  setTimeout(function() {
		$j(window).trigger('resize'); 
	  }, 1);
    });	
	
   $j('#tglFull').click(function() {
	  $j('body').removeClass("boxed");  
	  $j('body').addClass("fullwidth");
	  $j('body').removeClass("wide");
	  $j('.slick-initialized').slick('setPosition');
	  setTimeout(function() {
		$j(window).trigger('resize'); 
	  }, 1);
    });	
	
	$j('#tglDefault').click(function() { 
	  $j('body').removeClass("fullwidth");
	  $j('body').removeClass("boxed");
	  $j('body').removeClass("wide");
	  $j('.slick-initialized').slick('setPosition');
	  setTimeout(function() {
		$j(window).trigger('resize'); 
	  }, 1);
    });
	
	$j('#tglWide').click(function() { 
	  $j('body').removeClass("fullwidth");
	  $j('body').removeClass("boxed");
	  $j('body').addClass("wide");
	  $j('.slick-initialized').slick('setPosition');
	  setTimeout(function() {
		$j(window).trigger('resize'); 
	  }, 1);
    });	
});
