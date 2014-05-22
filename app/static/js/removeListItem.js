$(document).ready(function () {
  $("input[type='checkbox']").change(function() {
    // .parent() is <td>
    // .parent().parent() is <tr>
    $(this).parent().parent().hide();
    
    var itemNumber = $(this).attr("name");
    $.post("/listitem/" + itemNumber);
  });
});
