/* Project specific Javascript goes here. */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(".genre").chosen({search_contains:true});

$(".instrument").chosen({search_contains:true});

$(".fa-heart-o").click(function(){
    var song_id = $(this).parent('a').attr('id');
    console.log(song_id);
    $.ajax({
        type: "GET", //should be post
        url: '/logic/api/inc-likes/',
        data: {song_id : song_id},
        dataType: 'json',
        contentType: 'application/json',
        success: function(data){
            console.log(data);
            $(this).toggleClass("fa-heart-o fa-heart");
        },
        error : function(xhr,errmsg,err) {
            // Show an error
            //$('#results').html("<div class='alert-box alert radius' data-alert>"+
            //"Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});