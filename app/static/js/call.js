
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


function get_versions_one(package, most_failed_packages){
	/* This function populates the version dropdown of the first package, as soon as
	 * the package is selected.
	*/
	if(package == "None"){
		document.getElementById('version_one').style.display = 'none';
		return;
	}
	var package_name = package;
	var versions = [];
	for(var i = 0; i < most_failed_packages.length ; i++){
		if(most_failed_packages[i]['name'] == package_name)
			versions.push(most_failed_packages[i]['version']);
	}
	document.getElementById('package_one_version').options.length = 0;
	var package_select_id = document.getElementById('package_one_version');
	document.getElementById('version_one').style.display = "block";
	var opt = document.createElement('option');
    opt.innerHTML = "All";
    opt.value = "All";
    package_select_id.appendChild(opt);
	for(var i = 0; i < versions.length ; i++){
		var opt = document.createElement('option');
    	opt.innerHTML = versions[i];
    	opt.value = versions[i];
    	package_select_id.appendChild(opt);
	}
}


function get_versions_two(package, most_failed_packages){
	/* This function populates the version dropdown of the second package, as soon as
	 * the package is selected.
	*/
	if(package == "None"){
		document.getElementById('version_two').style.display = 'none';
		return;
	}
	var package_name = package;
	var versions = [];
	for(var i = 0; i < most_failed_packages.length ; i++){
		if(most_failed_packages[i]['name'] == package_name)
			versions.push(most_failed_packages[i]['version']);
	}
	document.getElementById('package_two_version').options.length = 0;
	var package_select_id = document.getElementById('package_two_version');
	document.getElementById('version_two').style.display = "block";
	var opt = document.createElement('option');
    opt.innerHTML = "All";
    opt.value = "All";
    package_select_id.appendChild(opt);
	for(var i = 0; i < versions.length ; i++){
		var opt = document.createElement('option');
    	opt.innerHTML = versions[i];
    	opt.value = versions[i];
    	package_select_id.appendChild(opt);
	}
}