// Button changes
$(document).ready(function () {
    $("#btnSpinner").click(function () {
        $(this).html(
            'Authenicating...'
        );
    });
});

$(document).ready(function () {
    $("#btnSubmit").click(function () {
        $(this).html(
            'Processing...'
        );
    });
});


// File Uploader Config
$(".custom-file-input").on("change", function () {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

// CHOSEN SELECT
$(".chosen-select").chosen({
    no_results_text: "Oops, nothing found for",
    width: "100%"
});


// JQUERY REPEATABLE
// More info: https://github.com/jenwachter/jquery.repeatable
$(function () {
    $("form .repeatable-container").repeatable({
        template: "#FormsAddMore"
    });
});


// Add More Btn
// TODO Use jquey repetable instead of this
$(document).ready(function () {
    var field = 1
    var max_fields = 10;
    var wrapper = $(".input_fields_wrap");
    var add_button = $(".add_field_button");
    $(add_button).click(function (e) {
        e.preventDefault();
        if (field < max_fields) {
            field++;
            $(".count_rows").val(field)
            var containerBlock = `<div><div class="row mt-2"><div class="col-md-4"><select class="chosen-select form-control" name="size_${field}" required><option selected value="40HC">40HC</option><option value="40DV">40DV</option><option value="20DV">20DV</option><option value="40RH">40RH</option><option value="20RF">20RF</option></select></div><div class="col-md-4"><input type="number" class="form-control h-input" name="quantity_${field}" placeholder="Quantity" required></div><div class="col-md-4"><input type="number" class="form-control h-input" name="price_${field}" placeholder="Price" required></div><a href="#" class="remove_field">Remove</a></div>`;
            $(wrapper).append(containerBlock);
        }
    });

    $(wrapper).on("click", ".remove_field", function (e) {
        e.preventDefault();
        $(this).parent('div').remove();
        field--;
        $(".count_rows").val(field)
    })
});

// FLATPICKR
// plugin for custom date picker More info:  https://flatpickr.js.org/
$(".dateSelector").flatpickr({
    dateFormat: "d/m/Y",
});

$(".dateTimeSelector").flatpickr({
    enableTime: true,
    dateFormat: "d/m/Y H:i",
});

$("#dateSelectorID").flatpickr({
    enableTime: true,
    dateFormat: "d/m/Y",
});

$(".pickr").flatpickr({
    dateFormat: "d/m/Y",
});

// PRINTTHIS
// More info: https://jasonday.github.io/printThis
$('#printInv').on("click", function () {
    $(".invoice-box").printThis({
        importCSS: true,
        importStyle: true,
    });
});

// More info: https://jasonday.github.io/printThis
$('#printRel').on("click", function () {
    $(".release-order").printThis({
        importCSS: true,
        importStyle: true,
    });
});

// HMTL2PDF
function generatePDF() {
    const element = document.getElementById("invoice");
    html2pdf()
        .set({
            html2canvas: {
                scale: 2
            },
            pagebreak: {
                pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
            }
        })
        .from(element)
        .save('harlos-proforma');
}

// Tagify
$('.tags').tagify({
    duplicates: false,
    tagTextProp: 'value',
});


// popovers initialization - on hover
$('[data-toggle="popover-hover"]').popover({
    html: true,
    trigger: 'hover',
    placement: 'right',
    content: function () {
        return '<img src="' + $(this).data('img') + '" />';
    }
});

// Progress Pie
$(function () {
    $(".pieprogress").progressPie({
        mode: $.fn.progressPie.Mode.COLOR,
        animate: true
    });
});


// Commas numbers on inputs
function updateTextView(_obj) {
    var num = getNumber(_obj.val());
    if (num == 0) {
        _obj.val('');
    } else {
        _obj.val(num.toLocaleString());
    }
}

function getNumber(_str) {
    var arr = _str.split('');
    var out = new Array();
    for (var cnt = 0; cnt < arr.length; cnt++) {
        if (isNaN(arr[cnt]) == false) {
            out.push(arr[cnt]);
        }
    }
    return Number(out.join(''));
}
$(document).ready(function () {
    $('.comNum').on('keyup', function () {
        updateTextView($(this));
    });
});


// Show PDF jquery plugin
$(document).ready(function () {
    $("#pdfBtn").click(function () {
        $("#pdfDiv").toggle();
    });
});

$(document).ready(function () {
    $("#pdfSlipBtn").click(function () {
        $("#pdfSlipDiv").toggle();
    });
});

// Dynamic select to trigger options on another select field
// Map your choices to your option value
var lookup = {
    'Dry Unit': ['40HC', '40DV', '20DV'],
    'Reffer': ['40RH', '20RF'],
};

// When an option is changed, search the above for matching choices | IDS
$('#UniOptions').on('change', function () {
    var selectValue = $(this).val();
    // Empty the target field
    $('#UniChoices').empty();
    // For each choice in the selected option
    for (i = 0; i < lookup[selectValue].length; i++) {
        // Output choice in the target field
        $('#UniChoices').append("<option value='" + lookup[selectValue][i] + "'>" + lookup[selectValue][i] + "</option>");
    }
});

// When an option is changed, search the above for matching choices | Classes
$('.UniOptions').on('change', function () {
    var selectValue = $(this).val();
    // Empty the target field
    $('.UniChoices').empty();
    // For each choice in the selected option
    for (i = 0; i < lookup[selectValue].length; i++) {
        // Output choice in the target field
        $('.UniChoices').append("<option value='" + lookup[selectValue][i] + "'>" + lookup[selectValue][i] + "</option>");
    }
});


// Date Range Filter on tables | Datatables & Boostrap Tables
function filterRows() {
    var from = $('#datefilterfrom').val();
    var to = $('#datefilterto').val();

    if (!from && !to) {
        return;
    }
    from = from || '1970-01-01';
    to = to || '2999-12-31';
    var dateFrom = moment(from);
    var dateTo = moment(to);

    // Contacts Table
    $('#contactsTable tr').each(function (i, tr) {
        var val = $(tr).find("td:nth-child(12)").text();
        var dateVal = moment(val, "DD/MM/YYYY");
        var visible = (dateVal.isBetween(dateFrom, dateTo, null, [])) ? "" : "none";
        $(tr).css('display', visible);
    });

    // Stock Table
    $('#stockTable tr').each(function (i, tr) {
        var val = $(tr).find("td:nth-child(4)").text();
        var dateVal = moment(val, "DD/MM/YYYY");
        var visible = (dateVal.isBetween(dateFrom, dateTo, null, [])) ? "" : "none";
        $(tr).css('display', visible);
    });

    // Petty Cash Reconciliation Table
    $('#pettycashrecoTable tr').each(function (i, tr) {
        var val = $(tr).find("td:nth-child(2)").text();
        var dateVal = moment(val, "DD/MM/YYYY");
        var visible = (dateVal.isBetween(dateFrom, dateTo, null, [])) ? "" : "none";
        $(tr).css('display', visible);
    });

}
$('#datefilterfrom').on("change", filterRows);
$('#datefilterto').on("change", filterRows);


// Select2
$(document).ready(function() {
    $('.multi').select2();
});

// Select2 Multiselect to hidden input usind IDs
$("#conditionInput").bind('keyup' , function(e){
    var ar = $(this).val().split(",");
    $("#conditions option").each(function(){
        if(ar.indexOf($(this).val()) != -1)
           $(this).attr("selected","selected");
    });
  });
$('#conditions').change(function(){
    $('#conditionInput').val($('#conditions').val());
});

// Select2 Multiselect to hidden input using Classes
$(".conditionInput").bind('keyup' , function(e){
    var ar = $(this).val().split(",");
    $(".conditions option").each(function(){
        if(ar.indexOf($(this).val()) != -1)
           $(this).attr("selected","selected");
    });
  });
$('.conditions').change(function(){
    $('.conditionInput').val($('.conditions').val());
});


// Display current date
function display_ct6() {
    var x = new Date()
    var ampm = x.getHours() >= 12 ? ' PM' : ' AM';
    hours = x.getHours() % 12;
    hours = hours ? hours : 12;
    var x1 = hours + ":" + x.getMinutes() + ":" + x.getSeconds() + ":" + ampm;
    document.getElementById('ct6').innerHTML = x1;
    display_c6();
}

function display_c6() {
    var refresh = 1000; // Refresh rate in milli seconds
    mytime = setTimeout('display_ct6()', refresh)
}
display_c6()



