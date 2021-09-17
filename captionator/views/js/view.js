function addContent(idx){
    var slice_len = 40;
    var source = $('#text-source').val();
    var selection = source.substr(idx,slice_len);
    var words = selection.split(' ');
    if (source.length > idx + selection.length){
        words.pop();
    }

    var textarea = $('#text-view').get(0);
    var addition = words.join(" ");
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
            updateTick();
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
