$(document).ready(function(){

    var socket = io.connect();

    // the socket.io documentation recommends sending an explicit package upon connection
    socket.on('connect', function() {
        socket.emit('connect', {data: 'I\'m connected!'});
    });

    $("input[type='checkbox'].sync").change(function() {
      socket.emit('value changed', {who: $(this).attr('id'), data: $(this).is(':checked')});
    });

    socket.on('update value', function(msg) {
      console.log(msg);
      console.log('About to change the value of ' + msg.who + ' from ' + $('input#'+msg.who).is(':checked') + ' to ' + msg.data);
      $('input#'+msg.who).prop("checked",(msg.data));
    });

});
