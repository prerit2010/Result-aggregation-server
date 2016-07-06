function func_os_user(os_user){
	var x_values = []
	var y_values = []
	for (var key in os_user) {
    	x_values.push(key);
    	y_values.push(os_user[key])
	}
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

function func_failed_installs(most_failed_packages){
	var x_values = []
	var y_values = []
	for (var key in most_failed_packages) {
    	x_values.push(key);
    	y_values.push(most_failed_packages[key])
	}
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