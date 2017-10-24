
$(document).ready(function(){

    $.get('/all_matches.json',function(data){
        console.log(data)
    var source = $("#matches-template").html();
    console.log('source', source)
    var template = Handlebars.compile(source);
    var user_data = [];
    data = data.slice(1,4) 
    for (var i = 0; i < data.length; i++) {
        user_data.push ({
                'user_id': data[i]['user_id'],
                'areas_score': data[i]['areas_score'],
                //hardcoded user score for demo purposes
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

        });
    } 
    var compiledHtml = template(user_data)
    // Add the compiled html to the page
    $('.content-placeholder').append(compiledHtml);
    }); 
});