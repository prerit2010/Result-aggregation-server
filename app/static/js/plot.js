function func(x_values, y_values){
	var data = [
		{
			x: x_values,
			y: y_values,
			type: 'bar'
		}
		];
		var layout = {
    		title: '',
    		showlegend: false
		};
		Plotly.newPlot('myDiv', data, layout, {displayModeBar: false});
}