$(document).ready(function(){
    $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  function ajax_login(){
    $.ajax({
      url: '/ajax-login',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response){
        console.log(response);
      },
      error: function(error){
        console.log(error);
      }
    });
  }

  $("#loginForm").submit(function(event){
    event.preventDefault();
    ajax_login();
  });

});