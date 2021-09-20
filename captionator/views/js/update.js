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
      $.ajax(url, {
        contentType: "application/json",
        type: "POST",
        data: JSON.stringify($("form").serializeObject()),
        complete: function( ) {
          btn_update
           .prop("disabled", false)
           .addClass("btn-primary").removeClass('btn-secondary')
           .find(".spinner-border").addClass('d-none');
        }
      });
      return false;
    });
    $.fn.serializeObject = function() {
       var o = {};
       var arr = this.serializeArray();
       $.each(arr, function() {
           if (o[this.name]) {
               if (!o[this.name].push) {
                   o[this.name] = [o[this.name]];
               }
               o[this.name].push(this.value || '');
           } else {
               o[this.name] = this.value || '';
           }
       });
       return o;
    };
  })
