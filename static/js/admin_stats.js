$(function() {
    var graph = $('#graph');
    if (graph.length > 0) {
        var data = graph.data('results');
        for (var k = 0; k < data.length; k++) {
            data[k][0] = new Date(data[k][0]).getTime();
        }
        $.plot(graph, [data], {xaxis: {mode: 'time'}});
    }

    $('#id_start, #id_end').datepicker();
});
