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



    if($('#user-matches').hasClass('active')) {
        //if session with user matches is selected on profile page
        //display matches 
        var count = 1 // page index for pagination
        console.log(count)
        getMatches(count)//
        var win = $(window);
        var isActive = false;
        // Each time the user scrolls
        win.scroll(function() {
        // End of the document reached?
            if (!isActive && $(document).height() - win.height() == win.scrollTop()) {
                isActive = true; //avoid multiple calls due to bouncing
                $('#loading').show();
                count +=1;
                getMatches(count);
                $('#loading').hide();
                isActive = false;
            }
        });    

        function getMatches(count){
            $.get('/matches.json/page/'+count.toString(), function(data){
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
            $('.content-placeholder').append(compiledHtml);
            });
        }

        function initPageNumbers() {
            //Get total rows number

            $.get('/total_rows.json', function (data){
                total_rows = parseInt(data.total_rows);
            })
            //Loop through every available page and output a page link
            var count = 1;
            var rows_per_page = 10;//PER_PAGE var in server.py


        }
        var num = "1";


    };
});        