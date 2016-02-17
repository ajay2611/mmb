/* Project specific Javascript goes here. */

$( window ).load(function() {
    $(".chosen").chosen({search_contains:true});
});

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

//var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

//$.ajaxSetup({
//    beforeSend: function(xhr, settings) {
//        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//            xhr.setRequestHeader("X-CSRFToken", csrftoken);
//        }
//    }
//});


 $(function(){

    check_follow = $("#check_follow").val();
    $(".follow").html("Following");
    $(".applied").hide();

    if(check_follow == "False"){
        $(".mybutton").css("display","none");
        $(".follow").html("Follow");
    }

    check_follow = $("#check_band_follow").val();
    $(".band_follow").html("Following");

    if(check_follow == "False"){
        $(".mybutton").css("display","none");
        $(".band_follow").html("Follow");
    }




    $('.check_like').each(function () {
        var id = this.id;
        var val = $("#"+id).val()

        //var splits = ($('.check_like').attr("id")).split(/(\d+)/);
        var splits = id.split(/(\d+)/);

        id = splits[1];
        if (val == "False"){
            $("#unlike_"+id).hide();
            $("#like_"+id).show();}
        else{
            $("#unlike_"+id).show();
            $("#like_"+id).hide();
        }
    });



    $('#id_type_1').change(function (event) {
        $('#div_id_instrument').hide();
    });

    $('#id_type_2').change(function (event) {
        $('#div_id_instrument').show();
    });

    $(".like").click(function(e){
        e && e.preventDefault();
        var $this = $(e.target);
        var song_id = $(this).attr('id');
        var splits = song_id.split(/(\d+)/);
        id = splits[1];
        $.ajax({
            type: "GET", //should be post
            url: '/logic/api/inc-likes/',
            data: {song_id : id},
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                if (data.not_authenticated){
                    alert('Not authorized.');
                    return;
                }
                $("#like_count_"+id).html(data['like_count']);
                $("#like_"+id).hide();
                $("#unlike_"+id).show();
    //            $this.toggleClass("fa-heart-o fa-heart text-active text-danger", 200);
            },
            error : function(xhr, errmsg, err){
                // Show an error
                //$('#results').html("<div class='alert-box alert radius' data-alert>"+
                //"Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>");
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });


    $(".unlike").click(function(e){
        e && e.preventDefault();
        var $this = $(e.target);
        var song_id = $(this).attr('id');
        var splits = song_id.split(/(\d+)/);
        id = splits[1];
        $.ajax({
            type: "GET", //should be post
            url: '/logic/api/dec-likes/',
            data: {song_id : id},
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                if (data.not_authenticated){
                    alert('Not authorized.');
                    return;
                }
                $("#like_count_"+id).html(data['like_count']);
                $("#unlike_"+id).hide();
                $("#like_"+id).show();
    //            $this.toggleClass("fa-heart-o fa-heart text-active text-danger", 200);
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

    $(".band_follow").click(function(e){
        e && e.preventDefault();
        var $this = $(e.target);
        var band_id = $(this).parent('a').attr('id');
        $.ajax({
        type: 'GET',
        url: "/logic/api/follow_band/",
        data: {band_id: band_id},
        dataType: 'json',
        contentType : "application/json",
        success: function(data){
            if(data.non_not_authenticated){
                alert("Not authorized");
                return;
            }
            $(".band_follow").html("Following");
            $(".mybutton").css("display","inline-table");
            $("#band_follow_count").html(data['band_follow_count']);
    //        $this.toggleClass("fa-eye, 200);

            }
        });
    });

    $(".band_unfollow").click(function(e){
        e && e.preventDefault();
        var $this = $(e.target);
        var band_id = $(this).parent('a').attr('id');
        $.ajax({
        type: 'GET',
        url: "/logic/api/unfollow_band/",
        data: {band_id: band_id},
        dataType: 'json',
        contentType : "application/json",
        success: function(data){
            if(data.non_not_authenticated){
                alert("Not authorized");
                return;
            }
            $(".band_follow").html("Follow");
            $(".mybutton").css("display","none");
            $("#band_follow_count").html(data['band_follow_count']);
    //        $this.toggleClass("fa-eye, 200);
            }
        });
    });

     $(".vacant").click(function(e){
        e && e.preventDefault();
        var $this = $(e.target);
        var band_id = $(this).parent('li').attr('data-id');
        var inst =  $(this).parent('li').attr('data-inst');
        var vac_type =  $(this).parent('li').attr('data-vac-type');
        $(".vacant").hide();
        $(".applied").show();
        $.ajax({
            type: 'GET',
            url: "/logic/api/apply-vacancy/",
            data: {band_id: band_id, inst: inst, type: vac_type},
            dataType: 'json',
            contentType : "application/json",
            success: function(data){
                if(data.non_not_authenticated){
                    alert("Not authorized");
                    return;
                }
            }
        });
    });



});
