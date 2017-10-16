$(document).ready(function(){
    $('#user-matches').on('click', function(evt){
        evt.preventDefault();
    });

    //convert user score to percentage to be displayed in progress bar
    Handlebars.registerHelper('percent', function(score){
      score = (score*100)/5
      return new Handlebars.SafeString(
      'style="width:'
      + score
      + '%"');
    });


    Handlebars.registerHelper('randompic', function(profile_pic){

        return 'https://source.unsplash.com/featured/640x480?dog'
    });
        

    if($('#user-matches').hasClass('active')) {
        //if session with user matches is selected on profile page
        //get data from server

        $.get('/matches.json', function(data){
            var source = $("#match-template").html();
            var template = Handlebars.compile(source);
            var user_info = data;
            console.log(user_info)
            var user_data = []; //json file from server serialize function
            for (var i = 0; i < data.length; i++) {
                user_data.push ({
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
                        'picture_url': 'data[i][picture_url]',
                        'hobbies': data[i]['hobbies'],
                        'pets': data[i]['pets'],
                                
                });
            }    

            var compiledHtml = template(user_data)
                // Add the compiled html to the page
            $('.content-placeholder').html(compiledHtml);
        
        });

    };
});        