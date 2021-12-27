var player,
    time_update_interval = 0;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('video-placeholder', {
        width: 600,
        height: 400,
        videoId: 'TBuIGBCF9jc',
        playerVars: {
            color: 'white'
        },
        events: {
            onReady: initialize
        }
    });
}

function initialize(){

    // Update the controls on load
    updateTimerDisplay();


    // Clear any old interval.
    clearInterval(time_update_interval);

    // Start interval to update elapsed time display and
    // the elapsed part of the progress bar every second.
    time_update_interval = setInterval(function () {
        updateTimerDisplay();
    }, 1000);



}


// This function is called by initialize()
function updateTimerDisplay(){
    // Update current time text display.
    $('#current-time').text(formatTime( player.getCurrentTime() ));
    $('#duration').text(formatTime( player.getDuration() ));
}







//$('.sentence').on('mouseup touchend', function (e) {
$('body').on('click', '[id^="sentence"]', function() {
    let t =$(this).val();
    player.seekTo(t);
});


$('#speed').on('change', function () {
    let rate=$(this).val();
    if (rate == 0.25)
    {
       player.setPlaybackRate(0.25);
    }
    else if (rate == 0.5)
    {
       player.setPlaybackRate(0.5);
    }
    else if (rate == 1)
    {
       player.setPlaybackRate(1);
    }
    else if (rate == 1.5)
    {
       player.setPlaybackRate(1.5);
    }
    else if (rate == 2) {
       player.setPlaybackRate(2);
    }

       //console.log(rate);
});





// Load video
$('body').on('click', '.thumbnail', function() {
    var leid = $('#leid');
    var v_placeholder = $('#video-placeholder');
    var url = $(this).attr('data-video-id');
    leid.hide();
    v_placeholder.hide();

    player.cueVideoById(url);
    $('.texts').hide();
    var text = $('ul#'+url);
    text.show();
    leid.show();
    v_placeholder.show();
});


// Helper Functions

function formatTime(time){
    time = Math.round(time);

    var minutes = Math.floor(time / 60),
        seconds = time - minutes * 60;

    seconds = seconds < 10 ? '0' + seconds : seconds;

    return minutes + ":" + seconds;
}


$('pre code').each(function(i, block) {
    hljs.highlightBlock(block);
});

$('body').on('click', '[id^="sentence"]', function() {
   $(this).addClass("animatedIn").delay(5000).queue(function(){
      $(this).removeClass("animatedIn").dequeue();
  });
});