// Search function
var search = function () {
    console.log("llamada por boton");
    $.getJSON($SCRIPT_ROOT + '/search', {
        s: $('input[name="q"]').val()
    }, function (data) {
        var array = data.result;
        var len = data.len;

        var str = "";
        for (var i = 0; i < len && i < 3; i++) {
            str = str + array[i] + "\r\n";
        }
        htmlstring = str.replace(/(\r\n|\n|\r)/gm, "<br>");
        $("#result").html(htmlstring);
    });
    return false;
}

// Triggers
$(function () {
    $('#searchbutton').bind('click', search);
    $('#searchbox').on('keyup', search);
});

