$(document).ready(function(){

    // check the number of rows in the table. If it is more than 1, then show the table
    // otherwise hide it.
    // This passes the number of rows to the hideShowIndex function below
    hideShowIndex($('#itemsTable tr').length);

    var socket = io.connect();

    // the socket.io documentation recommends sending an explicit package upon connection
    socket.on('connect', function() {
        //socket.emit('connect', {data: 'I\'m connected!'});
    });

    // Some special rules to deal with checkboxes
    $("input[type='checkbox'].sync").change(function() {
      socket.emit('checkbox changed', {who: $(this).attr('id'), data: $(this).is(':checked')});
    });

    socket.on('update checkbox', function(msg) {
      $('input#'+msg.who).prop("checked",(msg.data));
    });

    socket.on('insert row', function(msg) {
      var data = JSON.parse(msg);
      var $html = '<tr>\
        <td>\
          <input type="checkbox" class="sync" name="' + data.id + '" id="checkbox' + data.id + '" value="' + data.checked + '"/>\
        </td>\
        <td>' + data.item + '</td>\
        <td>' + data.creator + '</td>\
        <td>' + data.created + '</td></tr>';
      $('#itemsTable TBODY').append($html);
      hideShowIndex($('#itemsTable tr').length);
    });

    socket.on('connect_error', function() {
      alert("You have been idle too long. When you press OK, I will refresh and reconnect.");
      location.reload("True");
    });

    $('#btnClearList').click(function() {
      location.reload("True");
    });
});

function hideShowIndex(rc) {
  $('#itemsTable').toggle(rc > 1);
  $('#btnClearList').toggle(rc > 1);
  $('#emptyList').toggle(rc <= 1);
}
