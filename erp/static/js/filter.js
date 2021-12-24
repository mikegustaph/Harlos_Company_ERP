$(document).ready(function () {

  // Filter Available Stock
  var table = $('#stockTable').DataTable();
  $('#stock_available').on('click', function () {
    table
      .column(3)
      .search('Available', true, false)
      .draw();
  });

  // Filter Booked Stock
  var table = $('#stockTable').DataTable();
  $('#stock_booked').on('click', function () {
    table
      .column(3)
      .search('Booked', true, false)
      .draw();
  });

  // Filter on hold
  var table = $('#stockTable').DataTable();
  $('#stock_hold').on('click', function () {
    table
      .column(3)
      .search('On Hold', true, false)
      .draw();
  });

   // Filter on hold
  var table = $('#stockTable').DataTable();
  $('#stock_sold').on('click', function () {
    table
      .column(3)
      .search('Sold', true, false)
      .draw();
  });

  // Filter on Outwards Stock
  var table = $('#stockTable').DataTable();
  $('#stock_outwards').on('click', function () {
    table
      .column(3)
      .search('Outwards', true, false)
      .draw();
  });

  var ctable = $('#contactsTable').DataTable({
    "scrollX": false,
    "oLanguage": {
      "sLengthMenu": "_MENU_ records per page",
      "sZeroRecords": "Oops! nothing found",
      "sInfo": "Showing _START_ to _END_ of _TOTAL_ records",
      "sInfoEmpty": "Showing 0 to 0 of 0 records",
      "sInfoFiltered": "(filtered from _MAX_ total records)"
    },
    "lengthMenu": [
      [20, 30, 40, 50, -1],
      [20, 30, 40, 50, "All"]
    ],
    dom: 'Bfrtip',
         buttons: [
             'excelHtml5',
             'csvHtml5',
             {
                    extend: 'pdfHtml5',
                    orientation: 'landscape',
                    pageSize: 'LEGAL'
            }
         ],
    responsive: true
  });

  // Re-draw the table when the a date range filter changes
  $('.dateSelector').change(function () {
    table.draw();
    ctable.draw();
  });
});