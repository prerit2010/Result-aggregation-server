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
            showlegend: false,
            xaxis : {
                title : 'Operating Systems'
            },
            yaxis : {
                title : 'Number of users'
            }
        };
        Plotly.newPlot('os_user', data, layout, {displayModeBar: false});
}

function func_failed_installs_all(most_failed_packages){
    var x_values = []
    var y_values = []
    for(var i=0 ; i < most_failed_packages.length ; i++){
        var failed_package = most_failed_packages[i]['name'] + ' (' + most_failed_packages[i]['version'].split('(')[0] + ')';
        x_values.push(failed_package);
        y_values.push(most_failed_packages[i]['count']);
    }
    var data = [
        {
            x:  y_values,
            y: x_values,
            type: 'bar',
            orientation : 'h'
        }
        ];
        var layout = {
            title: '',
            showlegend: false,
            margin:{
                l:300
            },
            yaxis : {
                title : 'Package Names ( failed )'
            },
            xaxis : {
                title : 'Number of users'
            }
        };
        Plotly.newPlot('failed_package', data, layout, {displayModeBar: false});
}

function func_failed_installs(most_failed_packages){
    var x_values = []
    var y_values = []
    for(var i=0 ; i < most_failed_packages.length ; i++){
        var failed_package = most_failed_packages[i]['name'] + ' (' + most_failed_packages[i]['version'].split('(')[0] + ')';
        x_values.push(failed_package);
        y_values.push(most_failed_packages[i]['count']);
        if(i > 10){
            break;
        }
    }
    var data = [
        {
            x:  y_values,
            y: x_values,
            type: 'bar',
            orientation : 'h'
        }
        ];
        var layout = {
            title: '',
            showlegend: false,
            margin:{
                l:300
            },
            yaxis : {
                title : 'Package Names ( failed )'
            },
            xaxis : {
                title : 'Number of users'
            }
        };
        Plotly.newPlot('failed_package', data, layout, {displayModeBar: false});
}

function func_python_users(python_version){
    var x_values = []
    var y_values = []
    for (var key in python_version) {
        x_values.push(key);
        y_values.push(python_version[key]);
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
            xaxis : {
                title : 'Python versions'
            },
            yaxis : {
                title : 'Number of users'
            }
        };
        Plotly.newPlot('python_users', data, layout, {displayModeBar: false});

}

function func_os_user_for_package(system){
    var x_values = []
    var y_values = []
    for (var key in system) {
        x_values.push(key);
        y_values.push(system[key]);
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
            xaxis : {
                title : 'Operating System'
            },
            yaxis : {
                title : 'Number of users'
            }
        };
        Plotly.newPlot('os_user_by_package', data, layout, {displayModeBar: false});

}


function func_os_user_dist_for_package(system){
    var x_values = []
    var y_values = []
    for (var key in system) {
        x_values.push(key);
        y_values.push(system[key]);
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
            xaxis : {
                title : 'Distributions'
            },
            yaxis : {
                title : 'Number of users'
            }
        };
        Plotly.newPlot('os_user_dist_by_package', data, layout, {displayModeBar: false});

}