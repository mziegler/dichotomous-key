// script for key-out interface
// requires jquery
// "keyID" variable declared above script


// a JSON object that keeps track of this users session with the key
var state = {
  "keyID" : keyID, // which key is currently being used
  "useranswers": {}, // dict of (questionID, answer) pairs the user has answered so far
  "remainingtaxa": [], // list of remaining taxon ID's
  "eliminatedtaxa": [], // list of eliminated taxon ID's
  "action": [], // tuple describing state modification for the server to do
  }
  
// Send the old state to the server (with keyID, useranswers, and action).
// The server computes a new state, modifying useranswers according to the action,
// And looking up remaining taxa and eliminated taxa
function updateState() 
{
  $("body").append("<br />request: " + JSON.stringify(state));
  $.post("updatestate", JSON.stringify(state))
  .done( function(data)
  {
    
    $("body").append("<br />response: " + data);
    state = $.parseJSON(data);
    
    updateViews();
  })
  .fail( function()
  {
    alert("Something went wrong!  This is embarrassing.");
  });
}

function updateQuestionView()
{
  $.post("questions", JSON.stringify(state))
  .done( function(data)
  {
    $("#questionlist").html(data);
  });
}


// update the parts of the interface that depend on the key state
function updateViews()
{
  updateQuestionView();
  //TODO
}

function answerTrue(questionID)
{
  state.action = ['answer', questionID, true];
  updateState();
}

function answerFalse(questionID)
{
  state.action = ['answer', questionID, false];
  updateState();
}

function removeAnswer(questionID)
{
  state.action = ['removeanswer', questionID];
  updateState();
}

$(document).ready( function()
{
  updateState();
  answerTrue(1);
  answerFalse(2);
  removeAnswer(1);
});