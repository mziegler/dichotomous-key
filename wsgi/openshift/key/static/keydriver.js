// script for key-out interface
// requires jquery
// "keyID" variable declared above script


var state = {
  "keyID" : keyID,
  "useranswers": {}, // dict of (questionID, answer) pairs the user has provided
  "remainingtaxa": [], // list of remaining taxon ID's
  "eliminatedtaxa": [], // list of eliminated taxon ID's
  "action": [], // tuple describing state modification for the server to do
  }
  
// Send the old state to the server (with keyID, useranswers, and action).
// The server computes a new state, modifying useranswers according to the action,
// And looking up remaining taxa and eliminated taxa
function updateState() 
{
  $.post("updatestate", JSON.stringify(state))
  .done( function(data)
  {
    
    alert(data);
    state = $.parseJSON(data);
    
    // TODO: call routines for updating interface  
  })
  .fail( function()
  {
    alert("Something went wrong!  This is embarrassing.");
  });
}

$(document).ready(updateState);
