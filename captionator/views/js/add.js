  $(function() {
    $('.dropdown-menu li a').click(function(){
        var selection = $(this).text();
        $('#dropdown-caption-input').text(selection);
        $('#dropdown-caption-input').val(selection);
        var caption_images = $('#caption-images');
        var caption_text = $('#caption-text');
        if (selection == "By Text"){
            caption_images.addClass('d-none');
            caption_text.removeClass('d-none');
        } else {
            caption_text.addClass('d-none');
            caption_images.removeClass('d-none');
        }
        caption_text.resetCaptions();
        caption_images.resetCaptions();
    });

    $('#btn-cancel').click(function(){
        $(location).attr("href", "/");
        return false;
    });

    $('form').submit(function(e){
      e.preventDefault();
      var formData = new FormData(this)
      if (formData.get('text') == ""){
        formData.delete('text');
      }
      var files = formData.getAll('image').filter(file => file.size > 0);
      formData.delete('image');
      if (files.length != 0) {
         files.forEach(file => formData.append("image", file));
      }
      $.ajax("/add", {
        contentType: false,
        processData: false,
        cache: false,
        type: "POST",
        data: formData,
        success: function ( data ) {
          $(location).attr("href", "/update/" + data.id);
        }});
      return false;
    });

    function duplication(){
        $(this).clone()
            .change(duplication)
            .val("")
            .appendTo("#caption-images");
    }
    $('input[type=file]').change(duplication);

    $.fn.resetCaptions = function(){
        var inputs = $(this).find('.form-control')
        while(inputs.length > 1) { inputs.last().remove(); }
        inputs.val("");
    }
});