$(document).ready(function(){
    //mentees - best matches 
    $('#user-matches').on('click', function(evt){
        $('#user-matches').addClass('active')    
    });


    if($('#user-matches').hasClass('active')) {
        //if session with user matches is selected on profile page
        //display matches
        var matches = getAllMatches()//create global variable to be accessed by function later 
        var count = 1; // page index for pagination
        console.log(matches)
        getMatches(count);//
        var win = $(window);
        var isActive = false;
        // Each time the user scrolls
        win.scroll(function() {
            if ($(document).height() - win.height() - win.scrollTop() < 0.6) {
                isActive = true;
                $('#loading').show();
                count +=1;
                getMatches(count);
                isActive = false;
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

        }
        function getMatches(count){
            var dict = {
                'count' : count,
                'matches': matches}

            $.get('/matches', dict, function(data){
            var source = $("#match-template").html();
            var template = Handlebars.compile(source);
            var user_data = []; //json file from server serialize function
            for (var i = 0; i < data.length; i++) {
                user_data.push ({
                        'user_id': data[i]['user_id'],
                        'areas_score': data[i]['areas_score'],
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
            });
        };    
    function getAllMatches(){
        $.get('/all_matches.json', function(data){
        return data
        });//assing matches to json file   
    }; 

});