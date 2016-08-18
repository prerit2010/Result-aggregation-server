/* 
This file contails all the graphs that are plotted using plotly.js
*/


/* There are global setting applied to each plot. These involve
 * removal some button provided by plotly.js by default, and also
 * display the mode bar permanenly for each plot.
*/
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
    /* Plot a graph for different operating systems used by users on '/view/'
    */

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
    Plotly.newPlot('os_user', data, layout, mode_bar_global_settings); //applied global settings
}


function func_failed_installs(most_failed_packages){
    /* Plot a bar graph for most failed packages and limit the results
     * upto 10 only.
    */

    var x_values = []
    var y_values = []
    for(var i=0 ; i < most_failed_packages.length ; i++){
        var failed_package = most_failed_packages[i]['name'] + ' (' + most_failed_packages[i]['version'].split('(')[0] + ')';
        x_values.push(failed_package);
        y_values.push(most_failed_packages[i]['count']);
        if(i > 8){ // break as soon as top 10 packages are being added
            break;
        }
    }
    x_values.reverse();
    y_values.reverse();
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


function func_failed_installs_names(most_failed_packages){
    /* Plot a bar graph for most failed packages (top 10) grouped by their name only.
     * Versions are not taken into account here. 
    */

    var x_values = []
    var y_values = []
    for(var i=0 ; i < most_failed_packages.length ; i++){
        var failed_package = most_failed_packages[i]['name'];
        x_values.push(failed_package);
        y_values.push(most_failed_packages[i]['count']);
        if(i > 8)
            break;
    }
    x_values.reverse();
    y_values.reverse();
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
    /* Plot a bar graph for different python versions that are used by users
     * while executing the installation scripts. It accepts for 2 packages for comparison,
     * and plots only for first package if the second one is not selected for comparison.
    */

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
    if(python_version_two){ // only if second package is selected for comparison
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
    /* Plot a bar graph for different operating systems that are used by users
     * while executing the installation scripts. It accepts for 2 packages for comparison,
     * and plots only for first package if the second one is not selected for comparison.
    */

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
    if(os_users_two){ // only if second package is selected for comparison
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
    /* Plot a bar graph for different Linux distriubtions that are used by users
     * while executing the installation scripts. It accepts for 2 packages for comparison,
     * and plots only for first package if the second one is not selected for comparison.
     * This graph is not plotted (function is not called) if there is no linux user for this
     * package
    */

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
    /* Plot a line chart for the failed package to view the frequency of failure of this package
     * over the period of time. It accepts for 2 packages for comparison,
     * and plots only for first package if the second one is not selected for comparison.
     * This graph is not plotted (function is not called) if results are filted by a specific
     * workshop.
    */

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
