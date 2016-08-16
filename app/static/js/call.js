function SelectElement(valueToSelect)
{    
  document.getElementById('sel_workshop').value = valueToSelect;
}

function compare_button(){
  if(document.getElementById('sel2').value != "None" && document.getElementById('sel1').value != "None"){
    document.getElementById('submit_button').value = "Compare";
    document.getElementById('submit_button').disabled = false;
  }
  else{
    if(document.getElementById('sel1').value != "None"){
      document.getElementById('submit_button').value = "Submit";
      document.getElementById('submit_button').disabled = false;
    }
    else
      document.getElementById('submit_button').disabled = true;
  }
  return true;
}