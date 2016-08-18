function on_page_load(valueToSelect, most_failed_packages){
    /* This function is called by base.html as soon as the page loads.
     * It sets the workshop Id and also populates the versions dropdowns by
     * calling get_versions_one() and get_versions_two() if the package
     * selected is not None.
    */
    document.getElementById('sel_workshop').value = valueToSelect;
    if(!most_failed_packages)
        return;
    if(document.getElementById('package_one_name').value != "None"){
        document.getElementById('version_one').style.display = "block"; // Show the versions div
        get_versions_one(document.getElementById('package_one_name').value, most_failed_packages);
    }
    if(document.getElementById('package_two_name').value != "None"){
        document.getElementById('version_two').style.display = "block"; // Show the versions div
        get_versions_two(document.getElementById('package_two_name').value, most_failed_packages);
    }
}


function check_same_package(){
    var package_one_version = document.getElementById('package_one_version').value;
    var package_two_version = document.getElementById('package_two_version').value;
    var package_one_name = document.getElementById('package_one_name').value;
    var package_two_name = document.getElementById('package_two_name').value;
    if(package_two_name == package_one_name && package_one_version == package_two_version){
        alert("Same packages cannot be compared!");
        return false;
    }
    else
        return true;
}


function compare_button(){
    /* This functions decides between the values of submit button
     * ('Submit' or 'Compare'). If packages from both the dropdowns are selected,
     * the value is changed to 'Compare', otherwise it remains 'Submit'. It also disables
     * the button if no package is selected from the first dropdown of failed packages.
    */
    if(document.getElementById('package_two_name').value != "None" && document.getElementById('package_one_name').value != "None"){
        document.getElementById('submit_button').value = "Compare";
        document.getElementById('submit_button').disabled = false;
    }
    else{
        if(document.getElementById('package_one_name').value != "None"){
            document.getElementById('submit_button').value = "Submit";
            document.getElementById('submit_button').disabled = false;
        }
        else
            document.getElementById('submit_button').disabled = true;
    }
    return true;
}


function get_versions_one(package_name, most_failed_packages){
    /* This function populates the version dropdown of the first package, as soon as
     * the package is selected.
    */
    if(package_name == "None"){
        document.getElementById('version_one').style.display = 'none';
        return;
    }
    // Clear the versions dropdown before filling it
    document.getElementById('package_one_version').options.length = 0;
    var package_select_id = document.getElementById('package_one_version');
    document.getElementById('version_one').style.display = "block";
    // Create options for the versions drowpdown
    var opt = document.createElement('option');
    opt.innerHTML = "All";
    opt.value = "All";
    package_select_id.appendChild(opt);

    for(var i = 0; i < most_failed_packages.length ; i++){
        // find all the versions of this package and add option for each in dropdown
        if(most_failed_packages[i]['name'] == package_name){
            var opt = document.createElement('option');
            opt.innerHTML = most_failed_packages[i]['version'];
            opt.value = most_failed_packages[i]['version'];
            package_select_id.appendChild(opt);
        }
    }
}


function get_versions_two(package_name, most_failed_packages){
    /* This function populates the version dropdown of the second package, as soon as
     * the package is selected.
    */
    if(package_name == "None"){
        document.getElementById('version_two').style.display = 'none';
        return;
    }
    // Clear the versions dropdown before filling it
    document.getElementById('package_two_version').options.length = 0;
    var package_select_id = document.getElementById('package_two_version');
    document.getElementById('version_two').style.display = "block";
    // Create options for the versions drowpdown
    var opt = document.createElement('option');
    opt.innerHTML = "All";
    opt.value = "All";
    package_select_id.appendChild(opt);

    for(var i = 0; i < most_failed_packages.length ; i++){
        // find all the versions of this package and add option for each in dropdown
        if(most_failed_packages[i]['name'] == package_name){
            var opt = document.createElement('option');
            opt.innerHTML = most_failed_packages[i]['version'];
            opt.value = most_failed_packages[i]['version'];
            package_select_id.appendChild(opt);
        }
    }
}
