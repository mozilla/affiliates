(function($){
    $.fn.extend({ 
    	
    	colorSelect: function(options){
    		
    		var defaults = {
    			style : "colorSelect"
    		};
    		
    		var options = $.extend(defaults,options);
    		
    		
    		return this.each(function(){
				/* hide the current selected*/
				var select = $(this);
				$(this).hide();
				/*creaete wraper*/
				var container = $(this).wrap('<div id="selected-color"/>');
				$("#selected-color").append('<span class="current-color"><img src="img/zemoga/bg-color.png" alt="" /></span>');
				/* create items */
				var list = $('<ul />').insertAfter($(this));
				$("option", this).length
				var currentItem = 0;
				$("option", this).each(function () {
               		list.append('<li class="color-item" style="background-color:#'+$(this).val()+'"><img src="img/zemoga/bg-color.png" alt="" /></li>');
             	 });
				 list.wrap('<div class="content-items" />');
				$("#selected-color div.content-items").hide();
				$('<div class="hit-area"/>').insertAfter($('#selected-color div.content-items'));
				$("#selected-color div.hit-area").click(function() {
  					$("#selected-color div.content-items").show();
				});
				$("#selected-color div.hit-area").keydown(function(event) {
					console.log(event.keyCode);
					if(event.keyCode=='27'){
						$("#selected-color div.content-items").hide();
					}
				});
				
				$('#selected-color div.content-items ul li').each(function(index) {
    				$(this).click(function() {
  						
						$("#selected-color div.content-items").hide();
						var indexColor = index;
						$("option", select).each(function (indexOption) {
							if(indexOption == indexColor){
								$(this).attr("selected","selected");
								$("#selected-color span.current-color").css("background-color","#"+$(this).val());
							}	
						 });
					});
  				});
/*
				$("option", $(this)).each(function(){
					console.log(this);
				});    			
*/
    		});
    	}
 });
})(jQuery);
$(function(){
 	if($(".colorSelect")){					
		$(".colorSelect").colorSelect();
			
	}
});
