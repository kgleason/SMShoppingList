$(document).ready(function () {
  $("input[type='checkbox']").change(function() {
    // .parent() is <td>
    // .parent().parent() is <tr>
    $(this).parent().parent().hide();
  });
});
