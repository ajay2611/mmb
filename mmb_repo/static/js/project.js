/* Project specific Javascript goes here. */

$(".genre").chosen({search_contains:true});

$(".instrument").chosen({search_contains:true});

$("button").click(function(){
    $.ajax({
        type: "POST",
        url: '/api/inc-likes/',
        data: data,
        dataType: 'json',
        contentType: 'application/json',
        success: function(data){
            alert(data)
        }
    });
});

