// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
});


$(document).ready(function () {
            $('#table1').DataTable({
                dom: 'Bfrtip',
                buttons: [
                    {
                        extend: 'copy',
                        text: '<i class="fas fa-clone"></i>',
                        classname: 'btn btn-secondary',
                        titleAttr: 'Copy'
                    }
                ]
            });
        });