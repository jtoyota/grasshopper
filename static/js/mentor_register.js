
//Function to handle submission of areas of interest questionnaire
 $(document).ready(function(){
    // alert('howdy');
    $("#areas_of_interest").on('submit', function(evt) {
        evt.preventDefault();
        //check if user selected all radio buttons;
        var n = $( "input:checked" ).length;
        alert('howdy');
        if(n < 5) {
            alert("Bummer! You forgot to select an option.")
        };
        //serialize input to string;
        var formInputs = $("#areas_of_interest").serialize();
        //remove areas of interest questionnaire;
        $(evt.target).remove();

        $(".cover-heading").text("Tell us more about you!");
        
        $(".wrap").append("<label>What are some of your favorite hobbies or activities?</label><input type='text' id='hobby_input'>");

        //autocomplete hobbies and pets
        $.post("/areas_of_interest.json", formInputs, function (results) {
            // evt.preventDefault();
            debugger;
           
            $('#hobby_input').autocomplete({source: results});


        });
        //replace header
});    

});
