function addContent(idx){
    var slice_len = 20;
    var source = $('#text-source').html();
    var addition = source.substr(idx,slice_len);
    if (source.length > idx + addition.length){
        var chop_len = addition
            .split('')
            .reverse()
            .join('')
            .split(/\s/)[0]
            .length;
        if (chop_len < slice_len){
            addition = addition.slice(0, addition.length - chop_len);
        }
    }

    $('#text-view').append(addition);
    idx += addition.length;
    var view = $('.text-height');
    view.scrollTop(view.prop('scrollHeight'));
    return idx;
}

$(function() {
    $('#btn-back').click(function(){
        $(location).attr("href", "/");
        return false;
    });

    var idx = 0;
    var MIN_SPEED = 0;
    var MAX_SPEED = 10;
    var START_SPEED = (MAX_SPEED - MIN_SPEED)/2;
    var MULTIPLIER = 5000;
    var speed = START_SPEED;
    var timer = null;
    var paused = false;

    $('#speedRange')
        .val(START_SPEED)
        .attr('min', MIN_SPEED)
        .attr('max', MAX_SPEED)
        .change(function(){
            speed = $(this).val();
        });
    function updateTick() {
        if (!paused) {
            idx = addContent(idx);
        }
        if (timer != null) {
            clearTimeout(timer);
            timer = null;
        }
        if (speed != 0 && !paused){
            var timeout = MULTIPLIER / speed;
            timer = setTimeout(updateTick, timeout);
        }
    }

    function manage_display(val) {
        paused = val != 'auto';
        if ( val == "full" ){
            $('#text-source').show();
            $('#text-view').hide();
        } else {
            $('#text-source').hide();
            $('#text-view').show();
        }
        updateTick();
    }

    $('input[name=display]').click(function(){
        manage_display($(this).val())
    });
    manage_display($('input[name=display]:checked').val());
})
