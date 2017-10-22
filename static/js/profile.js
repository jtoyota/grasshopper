$(document).ready(function(){

      $(".users").on('click', function(evt) {
      // remove classes from all
      $(".users").removeClass("active");
      // add class to the one we clicked
      $(this).addClass("active");
      // stop the page from jumping to the top
      return false;
   });

    //mentees - best matches
    var matches;
    var perPage = 10;
    //get json from server;
    $.ajax({
        method: 'GET',
        url: '/all_matches.json',
        async: false,
        success: function(data){
            matches = data
            console.log(matches)
        }
    });

    //slice array
    function sliceArray(page){
        return matches.slice(perPage*(page-1),(perPage*page))
    }

    if($('#user-matches').hasClass('active')) {
        //if session with user matches is selected on profile page
        // var matches = getAllMatches()//create global variable to be accessed by function later 
        var count = 1; // page index for pagination
           
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
   
        //convert user score to percentage to be displayed in progress bar
        Handlebars.registerHelper('percent', function(score){
          score = (score*100)/5
          return new Handlebars.SafeString(
          'style="width:'
          + score
          + '%"');
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
                        'picture_url': 'http://loremflickr.com/320/240/dog?random',
                        'hobbies': data[i]['hobbies'],
                        'pets': data[i]['pets'],

                });
            }    
            var compiledHtml = template(user_data)
            // Add the compiled html to the page
            $('.content-placeholder').append(compiledHtml);    
        }    
    }            
});