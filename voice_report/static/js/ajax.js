$(function() {
    $('#addEventModal').submit(function(e) {
      var $form = $(this);
      $.ajax({
        type: $form.attr('post'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {
        console.log('success');
      }).fail(function() {
        console.log('fail');
      });
      //отмена действия по умолчанию для кнопки submit
      e.preventDefault(); 
    });
    $('#addLiveModal').submit(function(e) {
        var $form = $(this);
        $.ajax({
          type: $form.attr('post'),
          url: $form.attr('action'),
          data: $form.serialize()
        }).done(function() {
          console.log('success');
        }).fail(function() {
          console.log('fail');
        });
        //отмена действия по умолчанию для кнопки submit
        e.preventDefault(); 
      });
      $('#addNextModal').submit(function(e) {
        var $form = $(this);
        $.ajax({
          type: $form.attr('post'),
          url: $form.attr('action'),
          data: $form.serialize()
        }).done(function() {
          console.log('success');
        }).fail(function(error) {
          console.log(error);
        });
        //отмена действия по умолчанию для кнопки submit
        e.preventDefault(); 
      });
  });