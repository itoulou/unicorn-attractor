$(document).ready(function(){
    $(".side-nav-btn").click(function(e){
        e.stopPropagation();
        $("#side-nav").removeClass("remove"); 
    });
    $("#side-nav").click(function(e){
        e.stopPropagation(); 
    });
    $('body, html').click(function(e){
        $("#side-nav").addClass("remove");
    });
    $('[data-toggle="tooltip"]').tooltip();
});
