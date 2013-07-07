$(document).ready(function(){

    var plot2 = $.jqplot('grafico', [totales, totales_acum], {

        series:[
            {renderer:$.jqplot.BarRenderer},
            {xaxis:'x2axis', yaxis:'y2axis'}],
        title: 'Curva ABC',
        axesDefaults: {
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                angle: 30
            }
        },
        axes: {
            xaxis: {
                renderer: $.jqplot.CategoryAxisRenderer
            },
            x2axis: {
                renderer: $.jqplot.CategoryAxisRenderer
            },
            yaxis: {
                autoscale:true
            },
            y2axis: {
                autoscale:true
            }
        }
    });
});
