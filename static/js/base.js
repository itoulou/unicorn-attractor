$(document).ready(function(){
    $(".side-nav-btn").click(function(e){
        e.stopPropagation();
        $("#side-nav").removeClass("remove");
        $("#side-nav").animate({"width": "50%"}, 750);
    });
    $("#side-nav").click(function(e){
        e.stopPropagation(); 
    });
    $('body, html').click(function(e){
        $("#side-nav").animate({"width": "-50%"}, 750);
    });
    $('[data-toggle="tooltip"]').tooltip();
});
