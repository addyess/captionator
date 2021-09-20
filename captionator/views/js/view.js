function addContent(idx){
    var slice_len = 20;
    var source = $('#text-source').val();
    var addition = source.substr(idx,slice_len);
    if (source.length > idx + addition.length){
        var chop_len = addition
            .split('')
            .reverse()
            .join('')
            .split(/\s/)[0]
            .length;
        addition = addition.slice(0, addition.length - chop_len);
    }

    var textarea = $('#text-view').get(0);
    textarea.value += addition;
    if (textarea.selectionStart == textarea.selectionEnd) {
        textarea.scrollTop = textarea.scrollHeight;
    }
    idx += addition.length;
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
        idx = addContent(idx);
        if (timer != null) {
            clearTimeout(timer);
            timer = null;
        }
        if (speed != 0 && !paused){
            var timeout = MULTIPLIER / speed;
            timer = setTimeout(updateTick, timeout);
        }
    }
    $('#pause').click(function(){
        paused = !paused;
        $(this).children().fadeToggle(200);
        updateTick();
    })
    updateTick();
})
