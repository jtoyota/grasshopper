
//Function to handle submission of areas of interest questionnaire
 $(document).ready(function(){
    //html for hobbies questions; hidden until user fills out areas of interest form;
    $("#hobbies").hide();

    $("#areas_of_interest").on('submit', function(evt) {
        evt.preventDefault();
        //check if user selected all radio buttons;
        var n = $( "input:checked" ).length;
        if(n < 5) {
            alert("Bummer! You forgot to select an option.")
        };
        //serialize input to string;
        var formInputs = $("#areas_of_interest").serialize();
        //remove areas of interest questionnaire;
        $("#areas_of_interest_class").remove();
        //display hobbies form;
        $("#hobbies").show();
        //change title - could be done in the html 
        $(".cover-heading").text("Tell us more about you!");
        
        //autocomplete hobbies and pets
        $.post("/areas_of_interest.json", formInputs, function (results) {
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
                minLength: 0,
                source: function( request, response ) {
                // delegate back to autocomplete, but extract the last term
                response( $.ui.autocomplete.filter(
                 results, extractLast( request.term ) ) );
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
    $('#hobbies').on('submit', function(evt){
        evt.preventDefault();
        formInputs = $("#hobby_input").val().split(",");
        hobbies_list = [];
        //clear data
        //loop over list, remove white spaces and duplicates and append to obj
        formInputs.forEach(function(hobby){
            if (hobby !== ' ' && !hobbies_list.includes(hobby)) { 
            hobbies_list.push(hobby);
            }
        });  
        inputsDict = {'hobbies' : hobbies_list.join('|')}  
        console.log(hobbies_list);
        console.log(inputsDict);
        $.post("/hobbies_and_pets.json", inputsDict, function (results) {
            //do something
            evt.preventDefault()
            console.log(results)
        });     
    });
});