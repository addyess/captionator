  $(function() {
    $('#btn-cancel').click(function(){
        $(location).attr("href", "/");
        return false;
    });
    $('form').submit(function(e){
      e.preventDefault();
      var btn_update = $('#btn-update');
      btn_update
         .prop("disabled", true)
         .addClass("btn-secondary").removeClass('btn-primary')
         .find(".spinner-border").removeClass('d-none');
      var id = $('#id').val();
      var url = "/update/" + id;
      var formData = new FormData(this)
      $.ajax(url, {
        contentType: false,
        processData: false,
        cache: false,
        type: "POST",
        data: formData,
        complete: function( ) {
          btn_update
           .prop("disabled", false)
           .addClass("btn-primary").removeClass('btn-secondary')
           .find(".spinner-border").addClass('d-none');
        }
      });
      return false;
    });
  })
