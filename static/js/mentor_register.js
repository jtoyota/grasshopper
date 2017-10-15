
//Function to handle submission of areas of interest questionnaire
$(document).ready(function(){
    //html for hobbies questions; hidden until user fills out areas of interest form;
    $("#hobbies_and_pets_class").hide();
    //html for logging in with linkedin or creating new account with email/password
    //displayed only at last step;
    $("#create_account_class").hide();

    $("#areas_of_interest").on('submit', function(evt) {
        evt.preventDefault();
        //check if user selected all radio buttons;
        var n = $( "input:checked" ).length;
        if(n < 5) {
            alert("Bummer! You forgot to select an option.")
            evt.preventDefault();
        };
        //serialize input to string;
        var formInputs = $("#areas_of_interest").serialize();
        //remove areas of interest questionnaire;
        $("#areas_of_interest_class").remove();
        //display hobbies form;
        $("#hobbies_and_pets_class").show();
        //change title - could be done in the html 
        $(".cover-heading").text("Tell us more about you!");
        
        //autocomplete hobbies and pets
        $.post("/areas_of_interest.json", formInputs, function (results) {
            //for autocomplete
            function split( val ) {
                return val.split( /,\s*/ );
            }
            function extractLast( term ) {
                return split( term ).pop();
            }
 
            $( "#hobby_input" )
            // don't navigate away from the field on tab when selecting an item
            .on( "keydown", function( event ) {
                if ( event.keyCode === $.ui.keyCode.TAB &&
                    $( this ).autocomplete( "instance" ).menu.active ) {
                    event.preventDefault();
                }
            })
            .autocomplete({
                minLength: 3,
                source: function( request, response ) {
                // delegate back to autocomplete, but extract the last term
                response( $.ui.autocomplete.filter(
                 results.hobbies, extractLast( request.term ) ) );
                },
                focus: function() {
                // prevent value inserted on focus
                    return false;
                },
                select: function( event, ui ) {
                var terms = split( this.value );
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push( ui.item.value );
                // add placeholder to get the comma-and-space at the end
                terms.push( "" );
                this.value = terms.join( ", " );
                return false;
                }
            });

            $( "#pet_input" )
            // don't navigate away from the field on tab when selecting an item
            .on( "keydown", function( event ) {
                if ( event.keyCode === $.ui.keyCode.TAB &&
                    $( this ).autocomplete( "instance" ).menu.active ) {
                    event.preventDefault();
                }
            })
            .autocomplete({
                minLength: 0,
                source: function( request, response ) {
                // delegate back to autocomplete, but extract the last term
                response( $.ui.autocomplete.filter(
                 results.pets, extractLast( request.term ) ) );
                },
                focus: function() {
                // prevent value inserted on focus
                    return false;
                },
                select: function( event, ui ) {
                var terms = split( this.value );
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push( ui.item.value );
                // add placeholder to get the comma-and-space at the end
                terms.push( "" );
                this.value = terms.join( ", " );
                return false;
                }
            });        

        });
        //replace header
    });    
    $('#hobbies-pets').on('submit', function(evt){
        evt.preventDefault();
        //step 1 - prepare hobbies list
        //input comes in one string separated by comma and with extra spaces
        hobbiesInput = $("#hobby_input").val().split(",");
        hobbies_list = [];
        //clear data
        //loop over list, remove white spaces and duplicates and push to list
        hobbiesInput.forEach(function(hobby){
            if (hobby !== ' ' && !hobbies_list.includes(hobby)) { 
            hobbies_list.push(hobby.trim());
            }        
        });

        //step 2 - prepare pets list 
        petsInput = $("#pet_input").val().split(",");
        pets_list = [];
        //clear data
        //loop over list, remove white spaces and duplicates and push to list
        petsInput.forEach(function(pet){
            if (pet !== ' ' && !pets_list.includes(pet)) { 
            pets_list.push(pet.trim());
            }        
        });        
        //convert list to string and add to object
        inputsDict = {
            'hobbies' : hobbies_list.join('|'),
            'pets' : pets_list.join('|')
        }  
        $.post("/hobbies_and_pets.json", inputsDict).done(function(data){
            
        //remove hobbies and pets form;
        $("#hobbies_and_pets_class").remove();
        //display create account/log in with linkedin;
        $("#create_account_class").show();
        //change title - could be done in the html 
        $(".cover-heading").text("You're one step away!");

        });
    });
});