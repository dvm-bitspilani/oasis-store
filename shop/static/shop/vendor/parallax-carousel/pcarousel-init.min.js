
(function($){
	$(function(){
		var $carouselSlider = $('.parallax-gal-carousel-content');
		function carouselSlider() {
			$carouselSlider.slick({
				infinite: true,
				arrows: true,
				lazyLoad: 'ondemand',
				slidesToShow: 3,
				slidesToScroll: 3,
				responsive: [{
					breakpoint: 992,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 3
					}
				}, {
					breakpoint: 768,
					settings: {
						slidesToShow: 2,
						slidesToScroll: 2
					}
				}, {
					breakpoint: 560,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				}, {
					breakpoint: 321,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1,
						centerMode: true,
						centerPadding: '20px'
					}
				}]
			}).addClass('full-w-img').parents('.carousel-navigation-wrapper').addClass('slick-slider-enable');
			//$carouselSlider.slick('reInit');
		}
		function carouselParallax() {
				if($carouselSlider.hasClass('slick-initialized')){
					$carouselSlider.slick('unslick').removeClass('full-w-img').parents('.carousel-navigation-wrapper').removeClass('slick-slider-enable');
				}
				var $carousel = $('.parallax-gallery .parallax-gal-carousel');
				if (Modernizr.touch) {
				  var hammertime = new Hammer($('.parallax-gallery').get(0));
				  hammertime.on('swipeleft', function(evt) {  });
				  hammertime.on('swiperight', function(evt) {  });
				}
				$carousel.on('mouseenter touchstart', function(evt){  });
				$carousel.on('change',function(evt,ind){  });
				$carousel.ccCarouselParallax({
					autoPlay:false,
					ease:Quad.easeOut,
					selector:'.parallax-gal-slide',
					rows:[0,65,127,250],
					perspective:[200,300,400,500],
				});	
				if($carousel.width() < 600 ) {
					
				}
		}
		function toggleSlides(ww) {	
			var wW = ww ? ww : parseInt($(window).width());			
			carouselParallax();
			if(wW < 992) {
				carouselSlider();
			}

		}
		toggleSlides();
		// $(window).resize(function(){
		// 	var ww = parseInt($(window).width());
		// 	toggleSlides(ww);
			
		// });
	});
})(jQuery);		