
//Function to handle submission of areas of interest questionnaire
$("#areas_of_interest").on('submit', function(evt) {
    evt.preventDefault();
    //check if user selected all radio buttons;
    var n = $( "input:checked" ).length;
    if(n < 5) {
        alert("Bummer! You forgot to select an option.")
    };
    //serialize input to string;
    var formInputs = $("#areas_of_interest").serialize();
    console.log(formInputs);
    $.post("/areas_of_interest/", formInputs, function (results) {
        $(evt.target).remove();
        //replace headline nafter user clicked on continue
        console.log(results)
    });
    //replace header
    $(".cover-heading").text("Tell us more about you!");
    // add 
    $(".wrap").append('<label>What are some of your favorite hobbies or activities?</label><input type="text" id="hobby_input">');

});



















// function orderMelons(evt) {
//     evt.preventDefault();

//     var formInputs = $("#order-form").serialize();
//     $.post("/order-melons.json", formInputs, function (results) {
//         if (results.code == "OK") {
//             $('#order-status').html("<p>" + results.msg + "</p>");
//         }
//         else {
//             $('#order-status').addClass("order-error");
//             $('#order-status').html("<p><b>" + results.msg + "</b></p>");
//         }
//     });
// }

// $("#order-form").on('submit', orderMelons);
// // PART 1: SHOW A FORTUNE

// // Written now to use an inline function for the event handler,
// // and to use the $.load() method

// $('#get-fortune-button').on('click', function (evt) {
//     $("#fortune-text").load('/fortune');
// });


// // PART 2: SHOW WEATHER

// // Written now to use an inline function for handling the
// // AJAX success handler.

// function showWeather(evt) {
//     evt.preventDefault();

//     var url = "/weather.json?zipcode=" + $("#zipcode-field").val();

//     $.get(url, function (results) {
//         $("#weather-info").html(results.forecast);
//     });
// }

// $("#weather-form").on('submit', showWeather);


// // PART 3: ORDER MELONS

// // Written now to use inline function for the handling the AJAX
// // success handler, and to use $form.serialize

// function orderMelons(evt) {
//     evt.preventDefault();

//     var formInputs = $("#order-form").serialize();
//     $.post("/order-melons.json", formInputs, function (results) {
//         if (results.code == "OK") {
//             $('#order-status').html("<p>" + results.msg + "</p>");
//         }
//         else {
//             $('#order-status').addClass("order-error");
//             $('#order-status').html("<p><b>" + results.msg + "</b></p>");
//         }
//     });
// }

// $("#order-form").on('submit', orderMelons);