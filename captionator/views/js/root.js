  var $table = $('#table');

  $(function() {
    $table.bootstrapTable();
    $('#btn-add').click(add);
    $('#btn-view').click(view);
    $('#btn-update').click(update);
    $('#btn-delete').click(del_caption);
  })

  function add(){
      $(location).attr("href", "/add");
  }

  function view(){
      var selected = $('.selected').find('[name="id"]');
      if (selected.length == 1){
          $(location).attr("href", "/view/" + selected.attr('value'));
      }
  }

  function update(){
      var selected = $('.selected').find('[name="id"]');
      if (selected.length == 1){
          $(location).attr("href", "/update/" + selected.attr('value'));
      }
  }

  function del_caption(){
      var selected = $('.selected').find('[name="id"]');
      if (selected.length == 1){
          $.post({
            type: "DELETE",
            url: "/update/" + selected.attr('value'),
            success: function(){
              $(location).attr("href", "/");
            }
          });
      }
  }
