var lastScrollTop = 0;
$(window).scroll(function(event){
   var st = $(this).scrollTop();
   if (st > lastScrollTop){
       $("#delivery-banner").hide()
   } else {
       $("#delivery-banner").hide()
   }
   lastScrollTop = st;
});