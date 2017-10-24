$(document).ready(function(){

$(".feed").on('click', function(evt) {
    // remove classes from all
    $(".feed").removeClass("active");
      // add class to the one we clicked
    $(this).addClass("active");
    if $("events").hasClass('active'){
        alert("here!")
    }
    return false;
});

    $.get('/connection_requests/pending_requests.json',function(data){
        var source = $("#request-template").html();
        var template = Handlebars.compile(source);
        var user_data = []; //json file from server serialize function
        data = data.slice(0,3)
        for (var i = 0; i < data.length; i++) {
            user_data.push ({
                    'user_id': data[i]['mentee_info']['user_id'],
                    'first_name': data[i]['mentee_info']['first_name'],
                    'last_name': data[i]['mentee_info']['last_name'],
                    'title' : (data[i]['mentee_info']['positions']['total'] > 0 ? data[i]['mentee_info']['positions']['values'][0]['title'] : null),
                    'company' : (data[i]['mentee_info']['positions']['total'] > 0 ? data[i]['mentee_info']['positions']['values'][0]['company'] : null),
                    'picture_url': "../static/images/dog"+i+".jpg",
                    'mentorship_id': data[i]['mentorship_id']           
            });

        console.log(user_data)
        }
        var compiledHtml = template(user_data)
        console.log(compiledHtml)
        // Add the compiled html to the page
        $('.pending-placeholder').append(compiledHtml);  

    });   
    
    
});
