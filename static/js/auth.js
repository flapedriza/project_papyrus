$(document).ready(function () {
    $(".log-in-btn").click(function () {
        $("#register-section").removeClass("from-top-to-bottom").addClass("from-top");
        $("#log-in-section").removeClass("from-top").addClass("from-top-to-bottom");
    });
    $("#close_login").click(function () {
        $("#log-in-section").removeClass("from-top-to-bottom").addClass("from-top");
    });
    $(".register-btn").click(function () {
        $("#log-in-section").removeClass("from-top-to-bottom").addClass("from-top");
        $("#register-section").removeClass("from-top").addClass("from-top-to-bottom");
    });
    $("#close_register").click(function () {
        $("#register-section").removeClass("from-top-to-bottom").addClass("from-top");
    });
});