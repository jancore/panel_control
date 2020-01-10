$(document).ready(function () {
  $(window).keydown(function (event) {
    if (event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  $("#logout").click(function(){
    $("#btnReset").click();
  });

  //connect to the socket server.
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var number_cycle;
  //receive details from server
  socket.on('newnumber', function(msg) {
      console.log("Received number " + msg.number);
      number_cycle = msg.number;
      $('#current-cycle').html(number_cycle);
  });



});