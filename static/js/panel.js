$(document).ready(function () {
  $(window).keydown(function (event) {
    if (event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  $("#create").click(function () {
    $("#btnReset").click();
  });

  $("#logout").click(function () {
    $("#btnReset").click();
  });

  $("#btnReset").click(function () {
    $.ajax({
      url: "/command/reset?n_cycles=0",
      type: "get",
      success: function (response) {
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
      }
    });
    $("#cyclesField").disabled = true;
  });

  $("#btnStop").click(function () {
    $.ajax({
      url: "/command/stop?n_cycles=" + $('#cyclesField').val(),
      type: "get",
      success: function (response) {
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
      }
    });
  });

  $("#btnAceptarMarcha").click(function () {
    $.ajax({
    url: "/command/start?n_cycles=" + $('#cyclesField').val(),
    type: "get",
    success: function (response) {
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(textStatus, errorThrown);
    }
    });

    $("#cyclesField").disabled = true;
  });

  //connect to the socket server.
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var current_cycle, n_cycles;
  //receive details from server
  socket.on('newcycle', function(msg) {
      console.log("Received number " + msg.current_cycle + " " + msg.n_cycles);
      current_cycle = msg.current_cycle;
      n_cycles = msg.n_cycles
      $('#current-cycle').html(current_cycle);
      $('#num-cycles').html(n_cycles)
  });



});