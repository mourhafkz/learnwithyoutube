$(document).ready(function() {
//    function reload_js(src) {
//        $('script[src="' + src + '"]').remove();
//        $('<script>').attr('src', src).appendTo('body');
//    }

	$('form').on('submit', function(event) {
                var form_data = new FormData($('#upload-list')[0]);
                var list_wrapper = $('#list_wrapper');
                var video_list = $('#video_list');
                var leid = $('#leid');
//                var script = $('#reload');
                $('#loading-image').show();
                $('#results').hide();
                list_wrapper.hide();

                $.ajax({
                    type: 'POST',
                    url: '/process',
                    data: form_data,
                    contentType: false,
                    cache: false,
                    processData: false,
                })
                .done(function(data) {
                    if (data.error) {
                        $('#loading-image').hide();
                        $('#errorAlert').text(data.error).show();
                        $('#successAlert').hide();
                        $('#results').show();
                    }
                    else {
                        $('#loading-image').hide();
//                        script.remove();



    video_list.empty();
    video_list.append('<h2>Choose a video:  <span class="easy"> Easy </span>|<span class="intermediate"> Intermediate </span>|<span class="difficult"> Difficult </span></h2>');
    $('#video-placeholder').hide();
    leid.hide();
    leid.empty();


$.each( data, function( key, value ) {

      $.each( value, function( k, v ) {
      let text_id = k;
      leid.append('<ul id='+ text_id +' class="texts"></ul')
        var ul = $('#'+text_id);
            // iterate over timed_captions
            $.each( v.timed_captions, function( ke, ve ) {
                ul.append('<li id="sentence'+ke+'" value="'+ ve.start + '"><p>'+ ve.text+ '</p></li>');
            });
      // find thmbnails
      video_list.append('<img class="thumbnail '+ v.level+'" src="https://img.youtube.com/vi/'+ v.id+ '/0.jpg" data-video-id="'+v.id+'"/>');



      });


});



///--------------------------------------------------



                    }
                })

   list_wrapper.show();
//   leid.show();
   $('#results').show();
	var script = $('#reload');
	script.remove()
	$('body').append('<script id="reload" src="static/js/script.js"></script>');
	event.preventDefault();

    });
	});

