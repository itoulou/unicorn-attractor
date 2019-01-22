$(document).ready(function(){
     var sideNav = $("#side-nav");
    $(".side-nav-btn").click(function(e){
        e.stopPropagation();
        sideNav.css({"display": ""});
        sideNav.removeClass("remove-side-nav");
        sideNav.animate({"width": "70%"}, 300);
    });
    sideNav.click(function(e){
        e.stopPropagation(); 
        sideNav.removeClass("remove-side-nav");
    });
    $('body, html').click(function(e){
        sideNav.animate({"width": "-70%"}, 300);
        setTimeout(function() {
             sideNav.addClass("remove-side-nav");
        }, 400);
    });
    $('[data-toggle="tooltip"]').tooltip();
    $('.dropdown').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
    });
      
    $('.dropdown').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
    });
});
