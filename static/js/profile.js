$(document).ready(function(){

    $(".users").on('click', function(evt) {
    // remove classes from all
      $(".users").removeClass("active");
      // add class to the one we clicked
      $(this).addClass("active");
        if($('#find-users').hasClass('active')) {
            alert('here!')
        }//else if
        else if($('#pending-requests').hasClass('active')) {

            $('.content-placeholder').hide();
            var source = $("#requests").html();
            var template = Handlebars.compile(source);
            var requests_data = []; //json file from server serialize function
            data = pending_requests.slice(0,5)
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                requests_data.push ({
                        'active_since': data[i]['mentee_info']['active_since'],
                        'user_id': data[i]['mentee_info']['user_id'],
                        'first_name': data[i]['mentee_info']['first_name'],
                        'last_name': data[i]['mentee_info']['last_name'],
                        'title' : (data[i]['mentee_info']['positions']['total'] > 0 ? data[i]['mentee_info']['positions']['values'][0]['title'] : null),
                        'company' : (data[i]['mentee_info']['positions']['total'] > 0 ? data[i]['mentee_info']['positions']['values'][0]['company'] : null),
                        'picture_url': "../static/images/dog"+i+".jpg",
                        'location': "../static/images/background"+i+".jpg",
                        'mentorship_id': data[i]['mentorship_id'],   
                        'country': data[i]['mentee_info']['country'],
                        'hobbies': data[i]['mentee_info']['hobbies'],
                        'pets': data[i]['mentee_info']['pets'],
                        'fun': data[i]['mentee_info']['fun_facts'],
                        'summary':data[i]['mentee_info']['summary'],

                });
            }
            var compiledHtml = template(requests_data)
            // Add the compiled html to the page
            $('.pending-placeholder').append(compiledHtml);  

        }//else if pending
    return false;
  // stop the page from jumping to the top
    });


   var textAreas = document.getElementById('msg-placeholder');

    Array.prototype.forEach.call(textAreas, function(elem) {
        elem.placeholder = elem.placeholder.replace(/\\n/g, '\n');
    });   


    //convert user score to percentage to be displayed in progress bar

    Handlebars.registerHelper('percent', function(score){
      score = (score*100)/5
      return new Handlebars.SafeString(
      'style="width:'
      + score
      + '%"');
    });

    Handlebars.registerHelper('getbackground', function(background){
        console.log(background)
      return new Handlebars.SafeString(
      '"background-image: url('
      + background
      + ');"');
    });

    //mentees - best matches
    var matches;
    //results per page
    var perPage = 10;
    //pending requests;
    var pending_requests;

    //get json from server;
    $.ajax({
        method: 'GET',
        url: '/all_matches.json',
        async: false,
        success: function(data){
            matches = data
        }
    });
    $.ajax({
        method: 'GET',
        url: '/connection_requests/pending_requests.json',
        async: false,
        success:function(data){
        pending_requests =data
        }
    })

    //dog image generatorß

    //slice json to display results in page
    function sliceArray(page){
        return matches.slice(perPage*(page-1),(perPage*page))
    }//slice array

          if($('#user-matches').hasClass('active')) {
        //if session with user matches is selected on profile page
        // var matches = getAllMatches()//create global variable to be accessed by function later 
        var count = 1; // page index for pagination
        console.log(count)
        var data = sliceArray(count);
        sortData(data);   
        //
        var win = $(window);
        // Each time the user scrolls
        win.scroll(function() {
            if ($(document).height() - win.height() - win.scrollTop() < 0.6) {
                $('#loading').show();
                count +=1;
                var data = sliceArray(count);
                sortData(data);
            }
        });

        function sortData(data){
            var source = $("#match-template").html();
            var template = Handlebars.compile(source);
            var user_data = []; 
            for (var i = 0; i < data.length; i++) {
                user_data.push ({
                        'user_id': data[i]['user_id'],
                        'areas_score': data[i]['areas_score'],
                        //hardcoded user score for demo purposes
                        'user_score': [{score:5, title:'My Style'},{score:5, title: 'My Career'},{score:2, title:'My World'},{score:3, title:'My Craft'},{score:3, title: 'My life'}] ,
                        'first_name': data[i]['first_name'],
                        'last_name': data[i]['last_name'],
                        'active_since': moment(data[i]['active_since']).format('MMMM YYYY'),
                        'title' : (data[i]['positions']['total'] > 0 ? data[i]['positions']['values'][0]['title'] : null),
                        'company' : (data[i]['positions']['total'] > 0 ? data[i]['positions']['values'][0]['company'] : null),
                        'start_date' : moment(data[i]['start_date']).format('MMMM YYYY'),
                        'summary': data[i]['positions']['values'][0]['summary'],
                        'industry': data[i]['industry'],
                        'country': data[i]['country'],
                        'picture_url': "../static/images/dog"+i+".jpg",
                        'hobbies': data[i]['hobbies'],
                        'pets': data[i]['pets'],
                        'location': "../static/images/background"+i+".jpg"

                });
            } 
            var compiledHtml = template(user_data)
            // Add the compiled html to the page
            $('.content-placeholder').append(compiledHtml);    
        }    
    }//if

    else if($('#find-users').hasClass('active')) {
    alert('here!')
}//else if
    else if($('#pending-requests').hasClass('active')) {

        $('.content-placeholder').hide();
        var source = $("#requests").html();
        var template = Handlebars.compile(source);
        var requests_data = []; //json file from server serialize function
        data = pending_requests.slice(0,5)
        console.log(data)
        for (var i = 0; i < data.length; i++) {
            requests_data.push ({
                    'active_since': data[i]['mentee_info']['active_since'],
                    'user_id': data[i]['mentee_info']['user_id'],
                    'first_name': data[i]['mentee_info']['first_name'],
                    'last_name': data[i]['mentee_info']['last_name'],
                    'title' : (data[i]['mentee_info']['positions']['total'] > 0 ? data[i]['mentee_info']['positions']['values'][0]['title'] : null),
                    'company' : (data[i]['mentee_info']['positions']['total'] > 0 ? data[i]['mentee_info']['positions']['values'][0]['company'] : null),
                    'picture_url': "../static/images/dog"+i+".jpg",
                    'mentorship_id': data[i]['mentorship_id'],   
                    'country': data[i]['mentee_info']['country'],
                    'hobbies': data[i]['mentee_info']['hobbies'],
                    'pets': data[i]['mentee_info']['pets'],
                    'fun': data[i]['mentee_info']['fun_facts'],
                    'summary':data[i]['mentee_info']['summary'],

            });
    }
    var compiledHtml = template(requests_data)
    console.log(compiledHtml)
    // Add the compiled html to the page
    $('.pending-placeholder').append(compiledHtml);  

}//else if pending

});
