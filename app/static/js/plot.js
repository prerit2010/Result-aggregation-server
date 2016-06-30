function func_os_user(x_values, y_values){
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
		Plotly.newPlot('os_user', data, layout, {displayModeBar: false});
}

function func_failed_installs(x_values, y_values){
	var data = [
		{
			x: x_values,
			y: y_values,
			type: 'bar'
		}
		];
		var layout = {
    		title: '',
    		showlegend: false,
    		margin:{
    			b:200
  			}
		};
		Plotly.newPlot('failed_package', data, layout, {displayModeBar: false});
}