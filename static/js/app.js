$(document).ready(function () {
    $(".log-in-btn").click(function(){
        $("#log-in-section").removeClass("from-top").addClass("from-top-to-bottom");
    });
    $(".close").click(function(){
        $("#log-in-section").removeClass("from-top-to-bottom").addClass("from-top");
    });
});