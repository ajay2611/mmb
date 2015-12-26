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

 $(function(){
    $(".mybutton").css("display","none");



$(".fa-heart-o").click(function(e){
    e && e.preventDefault();
    var $this = $(e.target);
    var song_id = $(this).parent('a').attr('id');
    console.log(song_id);
    $.ajax({
        type: "GET", //should be post
        url: '/logic/api/inc-likes/',
        data: {song_id : song_id},
        dataType: 'json',
        contentType: 'application/json',
        success: function(data){
            if (data.not_authenticated){
                alert('Not authorized.');
                return;
            }
            console.log(data);
            $("#like_count_1").html(data['like_count']);
            $this.toggleClass("fa-heart-o fa-heart text-active text-danger", 200);
        },
        error : function(xhr, errmsg, err){
            // Show an error
            //$('#results').html("<div class='alert-box alert radius' data-alert>"+
            //"Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});

$(".follow").click(function(e){
    e && e.preventDefault();
    var $this = $(e.target);
    var user_id = $(this).parent('a').attr('id');
    $.ajax({
    type: 'GET',
    url: "/logic/api/follow/",
    data: {user_id: user_id},
    dataType: 'json',
    contentType : "application/json",
    success: function(data){
        if(data.non_not_authenticated){
        alert("Not authorized");
        return;
        }
        $(".follow").html("Following");
        $(".mybutton").css("display","inline-table");
        $("#following_count").html(data['following_count']);
        $("#followed_by_count").html(data['followed_by_count']);
//        $this.toggleClass("fa-eye, 200);

        }
    });
});

$(".unfollow").click(function(e){
    e && e.preventDefault();
    var $this = $(e.target);
    var user_id = $(this).parent('a').attr('id');
    $.ajax({
    type: 'GET',
    url: "/logic/api/unfollow/",
    data: {user_id: user_id},
    dataType: 'json',
    contentType : "application/json",
    success: function(data){
        if(data.non_not_authenticated){
        alert("Not authorized");
        return;
        }
        $(".follow").html("Follow");
        $(".mybutton").css("display","none");
        $("#followed_by_count").html(data['followed_by_count']);
        $("#following_count").html(data['following_count']);
//        $this.toggleClass("fa-eye, 200);
        }
    });
});

});
