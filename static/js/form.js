$(document).ready(function() {


$('body').on('mouseenter', "[id^='sentence'], [id^='speed']", function() {
      var video_id_from_parent = $(this).parent().attr('id');
      var item_no = $(this).prop('id').split("-").pop();
      var item_name = "#speed-"+video_id_from_parent+"-"+item_no;
        $(item_name).css("display","inline");

});


$('body').on('mouseleave', "[id^='sentence'], [id^='speed']", function() {
      var video_id_from_parent = $(this).parent().attr('id');
      var item_no = $(this).prop('id').split("-").pop();
      var item_name = "#speed-"+video_id_from_parent+"-"+item_no;
       $(item_name).css("display","none");
});

	$('form').on('submit', function(event) {
        var form_data = new FormData($('#upload-list')[0]);
        form_data.append("lang", $("#lang").val());
        form_data.append("method", $("#method").val());
        var list_wrapper = $('#list_wrapper');
        var video_list = $('#video_list');
        var leid = $('#leid');
        $('#loading-image').show();
        $('#results').hide();
        list_wrapper.hide();
//        console.log(form_data);
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
                                ul.append('<li id="sentence-'+text_id+'-'+ke+'" value="'+ ve.start + '" data-duration='+ ve.duration +'><p>'+ ve.text+ ' <select id="speed-'+text_id+'-'+ke+'" style="display:none;" > <option>0.25</option> <option>0.5</option> <option selected="selected">1</option> <option>1.5</option> <option>2</option> </select></p></li>');
                            });
                      // find thmbnails
                      video_list.append('<img class="thumbnail '+ v.level+'" src="https://img.youtube.com/vi/'+ v.id+ '/0.jpg" data-video-id="'+v.id+'"/>');

                        });

                });

            }
        })

       list_wrapper.show();
    //   leid.show();
       $('#results').show();
//        var script1 = $('#reload1');
//        var script2 = $('#reload2');
//        script1.remove()
//        script2.remove()
//        $('body').append('<script id="reload2" src="static/js/script.js"></script>');
//        $('body').append('<script id="reload1" src="static/js/form.js"></script>');
        event.preventDefault();

    });
});

