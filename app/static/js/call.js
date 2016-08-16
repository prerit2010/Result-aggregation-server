function on_page_load(valueToSelect, most_failed_packages)
{    
  document.getElementById('sel_workshop').value = valueToSelect;
  if(!most_failed_packages)
  	return;
  if(document.getElementById('package_one_name').value != "None"){
  	document.getElementById('version_one').style.display = "block";
  	get_versions_one(document.getElementById('package_one_name').value, most_failed_packages);
  }
  if(document.getElementById('package_two_name').value != "None"){
  	document.getElementById('version_two').style.display = "block";
  	get_versions_two(document.getElementById('package_two_name').value, most_failed_packages);
  }
}

function compare_button(){
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
    opt.innerHTML = "None";
    opt.value = null;
    package_select_id.appendChild(opt);
	for(var i = 0; i < versions.length ; i++){
		var opt = document.createElement('option');
    opt.innerHTML = versions[i];
    opt.value = versions[i];
    package_select_id.appendChild(opt);
	}
}

function get_versions_two(package, most_failed_packages){
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
    opt.innerHTML = "None";
    opt.value = null;
    package_select_id.appendChild(opt);
	for(var i = 0; i < versions.length ; i++){
		var opt = document.createElement('option');
    opt.innerHTML = versions[i];
    opt.value = versions[i];
    package_select_id.appendChild(opt);
	}
}