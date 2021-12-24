 // Marketing - Campaigns
 $(document).ready(function () {
     var campaignsTb = $('#campaignsTable').DataTable({
         "scrollX": true,
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
     campaignsTb.draw();
 });


 // CRM - Leads
 $(document).ready(function () {
     var leadsTb = $('#leadsTable').DataTable({
         "scrollX": true,
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
         // SearchPanes
         columnDefs: [{
             searchPanes: {
                 show: true,
                 container: '.searchPanes',
                 layout: 'columns-1',
                 cascadePanes: true,
                 viewTotal: true
             },
             targets: [2, 3, 4, 5, 6, 7, 8, 9, 10],
         }],
         responsive: true,
         deferRender: true
     });
     leadsTb.draw();
 });

 $(document).ready(function () {
     var table = $('#stockTable').DataTable({
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
         // SearchPanes
         columnDefs: [{
             searchPanes: {
                 show: true,
                 container: '.searchPanes',
                 layout: 'columns-1',
                 cascadePanes: true,
                 viewTotal: true
             },
             targets: [3, 4, 5],
         }],
         responsive: true,
         deferRender: true
     });

     table.draw();
 });

 // Advanced filtering - CRM - leadsTable
 $(document).ready(function () {
     var table = $('#leadsTable').DataTable();
     new $.fn.dataTable.SearchPanes(table, {});
     table.searchPanes.container().insertAfter('#spButton').addClass('collapse').attr("id", "spCont");
 });

 $(document).ready(function () {
     var table = $('#leadsTable').DataTable();
     new $.fn.dataTable.SearchBuilder(table, {});
     table.searchBuilder.container().insertAfter('#sbButton').addClass('collapse').attr("id", "sbCont");
 });


 // Advanced filtering - CRM - leadsTable
 $(document).ready(function () {
     var table = $('#stockTable').DataTable();
     new $.fn.dataTable.SearchPanes(table, {});
     table.searchPanes.container().insertAfter('#spButton').addClass('collapse').attr("id", "spCont");
 });

 // CRM - Deals
 $(document).ready(function () {
     var dealsTb = $('#dealsTable').DataTable({
         "scrollX": true,
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
     dealsTb.draw();
 });


 // CRM - Accounts
 $(document).ready(function () {
     var accountsTb = $('#accountsTable').DataTable({
         "scrollX": true,
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
     accountsTb.draw();
 });


 // CRM - Activities
 $(document).ready(function () {
     var activitiesTb = $('#activitiesTable').DataTable({
         "scrollX": true,
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
         responsive: true
     });
     activitiesTb.draw();
 });


 // CRM - Contacts
 $(document).ready(function () {
     var crmcTb = $('#crmcTable').DataTable({
         "scrollX": true,
         "oLanguage": {
             "sLengthMenu": "Display _MENU_ records per page",
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

     crmcTb.draw();
 });


 // Roles Viewer
 $(document).ready(function () {
     var table = $('.rolesTable').DataTable({
         searching: false,
         paging: false,
         info: false
     });
 });

 // Global
 $(document).ready(function () {
     var contTb = $('#globalTable').DataTable({
         "scrollX": true,
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
     contTb.draw();
 });