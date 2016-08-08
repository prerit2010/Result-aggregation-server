function func_os_user(os_user){
    var x_values = []
    var y_values = []
    for(var i = 0, size = os_user.length; i < size ; i++){
       x_values.push(os_user[i][0]);
       y_values.push(os_user[i][1]);
    }
    var data = [
        {
            x: x_values,
            y: y_values,
            type: 'bar'
        }
    ];

    var annotations_content = [];
    for( var i = 0 ; i < x_values.length ; i++ ){
      var result = {
        x: x_values[i],
        y: y_values[i],
        text: y_values[i],
        xanchor: 'center',
        yanchor: 'bottom',
        showarrow: false
      };
      annotations_content.push(result);
    }

    var layout = {
        title: '',
        showlegend: false,
        xaxis : {
            title : 'Operating Systems'
        },
        yaxis : {
            title : 'Number of users'
        },
        annotations: annotations_content
    };
    Plotly.newPlot('os_user', data, layout);
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
    Plotly.newPlot('failed_package', data, layout);
}

function func_failed_installs(most_failed_packages){
    var x_values = []
    var y_values = []
    for(var i=0 ; i < most_failed_packages.length ; i++){
        var failed_package = most_failed_packages[i]['name'] + ' (' + most_failed_packages[i]['version'].split('(')[0] + ')';
        x_values.push(failed_package);
        y_values.push(most_failed_packages[i]['count']);
        if(i > 8){
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

    var annotations_content = [];
    for( var i = 0 ; i < x_values.length ; i++ ){
      var result = {
        x: y_values[i],
        y: x_values[i],
        text: "       " + y_values[i].toString(),
        xanchor: 'bottom',
        yanchor: 'center',
        showarrow: false
      };
      annotations_content.push(result);
    }
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
            },
            annotations: annotations_content
        };
        Plotly.newPlot('failed_package', data, layout);
}

function func_failed_installs_names_all(most_failed_packages){
    var x_values = []
    var y_values = []
    for(var i=0 ; i < most_failed_packages.length ; i++){
        var failed_package = most_failed_packages[i]['name'];
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
        Plotly.newPlot('failed_package_names', data, layout);
}

function func_failed_installs_names(most_failed_packages){
    var x_values = []
    var y_values = []
    for(var i=0 ; i < most_failed_packages.length ; i++){
        var failed_package = most_failed_packages[i]['name'];
        x_values.push(failed_package);
        y_values.push(most_failed_packages[i]['count']);
        if(i > 8)
            break;
    }
    var data = [
        {
            x:  y_values,
            y: x_values,
            type: 'bar',
            orientation : 'h'
        }
    ];

    var annotations_content = [];
    for( var i = 0 ; i < x_values.length ; i++ ){
      var result = {
        x: y_values[i],
        y: x_values[i],
        text: "       " + y_values[i].toString(),
        xanchor: 'bottom',
        yanchor: 'center',
        showarrow: false
      };
      annotations_content.push(result);
    }

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
        },
        annotations: annotations_content
    };
    Plotly.newPlot('failed_package_names', data, layout);
}

function func_python_users(python_version){
    var x_values = []
    var y_values = []
    for(var i = 0, size = python_version.length; i < size ; i++){
       x_values.push(python_version[i][0]);
       y_values.push(python_version[i][1]);
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
        Plotly.newPlot('python_users', data, layout);

}

function func_os_user_for_package(system){
    var x_values = []
    var y_values = []
    for(var i = 0, size = system.length; i < size ; i++){
       x_values.push(system[i][0]);
       y_values.push(system[i][1]);
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
        Plotly.newPlot('os_user_by_package', data, layout);

}


function func_os_user_dist_for_package(system){
    var x_values = []
    var y_values = []
    for(var i = 0, size = system.length; i < size ; i++){
       x_values.push(system[i][0]);
       y_values.push(system[i][1]);
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
        Plotly.newPlot('os_user_dist_by_package', data, layout);

}


function func_failed_package_time_series(create_time){
    var x_values = []
    var y_values = []
    for (var key in create_time) {
        x_values.push(key);
        y_values.push(create_time[key]);
    }
    var data = [
      {
        x: x_values,
        y: y_values,
        type: 'scatter'
      }
    ];
    var layout = {
            title: '',
            xaxis : {
                title : 'Time'
            },
            yaxis : {
                title : 'Number of users'
            }
        };

    Plotly.newPlot('create_time', data, layout);
}