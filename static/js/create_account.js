$(document).ready(function(){

    $("#linkedin").mouseover(function(){
        $( "#linkedin" )
        .html('<img src="../static/signin_with_linkedin-buttons/Retina/Sign-In-Small---Active.png">' );
    }); 
    $("#linkedin").mouseout(function(){
        $( "#linkedin" )
        .html('<img src="../static/signin_with_linkedin-buttons/Retina/Sign-In-Small---Default.png">' );
    }); 
});

