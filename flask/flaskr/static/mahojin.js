(function($){
	var score = 0;
	var game_end = false;
 	var score_string = document.getElementById('score_string');
	$.fn.rotate_box = function(){

		var	elm = $(this),
			elm_in = $('.inner', this),
			btn = $('.face, .back', elm),
			deg = 0,
			turn = false,
			turn_cls = 'reverse';

		var rotate_anm = function(){
			elm_in.css({
				'transform' : 'rotateY(' + deg * -2 + 'deg)'
			});
		};

		var rotate = function(){

			setTimeout(function(){
				rotate_anm();
				if( deg == 45 ){
					if( turn === false ){
						elm.addClass(turn_cls);
					} else {
						elm.removeClass(turn_cls);
					}
					deg = 315;
				}
				if( deg <= 45 ){
					deg += 3;
					rotate();
				} else if( deg < 360 && deg > 45 ) {
					deg += 3;
					rotate();
				} else {
					deg = 0;
					elm_in.attr('style', '');
					if( turn === false ){
						turn = true;
					} else {
						turn = false;
					}
				}
			}, 5);
		};

		btn.click(function(){
			if(game_end == false){
				if(elm.hasClass("reversed") == false ){
					rotate();
					elm.addClass("reversed");

					if(elm.hasClass("joker") == true){
						score += 100;
						$("p.score_string").text(score)
						game_end = true;

					}else{
						score += 100;
						$("p.score_string").text(score);
					}
				}else{
				}
			}


		});
	};
})(jQuery);

$('.card').each(function(){
	$(this).rotate_box();

});
