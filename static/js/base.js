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
    $(".delete-issue").click(function(){
       return confirm("Are sure you want to delete your Issue?"); 
    });
    $('#myModal').on('shown.bs.modal', function () {
        $('#myInput').focus();
    });
    // $(".votes-chevron-btn").click(function(e){
    //     e.preventDefault();
    //     $(".votes-chevron-btn").toggleClass("voted");
    //     $.post(window.location.pathname, function(data){
    //     });
    // });
});