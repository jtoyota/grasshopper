$(document).ready(function(){

    $("#linkedin")
    .mouseenter(function(){
        $( this )
        .html('<img src="../static/signin_with_linkedin-buttons/Retina/Sign-In-Small---Active.png">' );
    })
    .mouseleave(function(){
        $( this )
        .html('<img src="../static/signin_with_linkedin-buttons/Retina/Sign-In-Small---Default.png">' );
    }); 
});

