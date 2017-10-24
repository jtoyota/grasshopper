$(document).ready(function(){

  var context = [ {'val':
                            {'title': "My_World", 'value': 4},

                          
                        
                  }
                ];

  // Grab the template script
  var script = $("#graph").html();

  // Compile the template
  var template = Handlebars.compile(script);

  // Define our data object

  // Pass our data to the template
  var theCompiledHtml = template(context:data);

  // Add the compiled html to the page
  $('.content-placeholder').html(theCompiledHtml);
}); 


