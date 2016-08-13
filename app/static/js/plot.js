var mode_bar_global_settings = {
    modeBarButtonsToRemove: [
        'sendDataToCloud',
        'hoverCompareCartesian',
        'hoverClosestCartesian',
        'zoom2d'
    ],
    displaylogo: false,
    displayModeBar: true
}


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
    Plotly.newPlot('os_user', data, layout, mode_bar_global_settings);
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
    Plotly.newPlot('failed_package', data, layout, mode_bar_global_settings);
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
    Plotly.newPlot('failed_package', data, layout, mode_bar_global_settings);
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
    Plotly.newPlot('failed_package_names', data, layout, mode_bar_global_settings);
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
    Plotly.newPlot('failed_package_names', data, layout, mode_bar_global_settings);
}

function func_python_users(python_version_one, python_version_two, package_name_one, package_name_two){
    var x_values = [];
    var y_values = [];
    for(var i = 0, size = python_version_one.length; i < size ; i++){
       x_values.push(python_version_one[i][0]);
       y_values.push(python_version_one[i][1]);
    }
    var trace1 = {
        x: x_values,
        y: y_values,
        name: package_name_one,
        type: 'bar'
    };
    if(python_version_two){
        var x_values = [];
        var y_values = [];
        for(var i = 0, size = python_version_two.length; i < size ; i++){
           x_values.push(python_version_two[i][0]);
           y_values.push(python_version_two[i][1]);
        }
        var trace2 = {
            x: x_values,
            y: y_values,
            name: package_name_two,
            type: 'bar'
        };

        var data = [trace1, trace2];
    }
    else
        var data = [trace1]

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
        barmode: 'group',
        xaxis : {
            title : 'Python versions'
        },
        yaxis : {
            title : 'Number of users'
        },
        annotations: annotations_content
    };
    Plotly.newPlot('python_users', data, layout, mode_bar_global_settings);

}

function func_os_user_for_package(os_users_one, os_users_two, package_name_one, package_name_two){
    var x_values = [];
    var y_values = [];
    for(var i = 0, size = os_users_one.length; i < size ; i++){
       x_values.push(os_users_one[i][0]);
       y_values.push(os_users_one[i][1]);
    }
    var trace1 = {
        x: x_values,
        y: y_values,
        name: package_name_one,
        type: 'bar'
    };
    if(os_users_two){
        var x_values = [];
        var y_values = [];
        for(var i = 0, size = os_users_two.length; i < size ; i++){
           x_values.push(os_users_two[i][0]);
           y_values.push(os_users_two[i][1]);
        }
        var trace2 = {
            x: x_values,
            y: y_values,
            name: package_name_two,
            type: 'bar'
        };

        var data = [trace1, trace2];
    }
    else
        var data = [trace1];

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
        barmode: 'group',
        xaxis : {
            title : 'Python versions'
        },
        yaxis : {
            title : 'Number of users'
        },
        annotations: annotations_content
    };
    Plotly.newPlot('os_user_by_package', data, layout, mode_bar_global_settings);

}


function func_os_user_dist_for_package(linux_dist_package_one, linux_dist_package_two, package_name_one, package_name_two){
    var x_values = [];
    var y_values = [];
    for(var i = 0, size = linux_dist_package_one.length; i < size ; i++){
       x_values.push(linux_dist_package_one[i][0]);
       y_values.push(linux_dist_package_one[i][1]);
    }
    var trace1 = {
        x: x_values,
        y: y_values,
        name: package_name_one,
        type: 'bar'
    };
    if(linux_dist_package_two){
        var x_values = [];
        var y_values = [];
        for(var i = 0, size = linux_dist_package_two.length; i < size ; i++){
           x_values.push(linux_dist_package_two[i][0]);
           y_values.push(linux_dist_package_two[i][1]);
        }
        var trace2 = {
            x: x_values,
            y: y_values,
            name: package_name_two,
            type: 'bar'
        };

        var data = [trace1, trace2];
    }
    else
        var data = [trace1];

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
        showlegend: true,
        barmode: 'group',
        xaxis : {
            title : 'Linux Distributions'
        },
        yaxis : {
            title : 'Number of users'
        },
        annotations: annotations_content
    };
    Plotly.newPlot('os_user_dist_by_package', data, layout, mode_bar_global_settings);

}


function func_failed_package_time_series(create_time_package_one, create_time_package_two, package_name_one, package_name_two){
    var x_values = [];
    var y_values = [];
    for (var key in create_time_package_one) {
        x_values.push(key);
        y_values.push(create_time_package_one[key]);
    }
    var trace1 = {
        x: x_values,
        y: y_values,
        name: package_name_one,
        type: 'scatter'
    };
    if(create_time_package_two){
        var x_values = [];
        var y_values = [];
        for (var key in create_time_package_two) {
            x_values.push(key);
            y_values.push(create_time_package_two[key]);
        }
        var trace2 = {
            x: x_values,
            y: y_values,
            name: package_name_two,
            type: 'scatter'
        };

        var data = [trace1, trace2];
    }
    else
        var data = [trace1];

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
        barmode: 'group',
        xaxis : {
            title : 'Time'
        },
        yaxis : {
            title : 'Number of users'
        },
        annotations: annotations_content
    };
    Plotly.newPlot('create_time', data, layout, mode_bar_global_settings);

}