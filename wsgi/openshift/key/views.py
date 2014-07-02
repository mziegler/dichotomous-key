import json

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

import key.keylogic as keylogic
from key.models import Key



"""Parse JSON out from the POST request body"""
def loadstateJSON(request):
  s = request.body.decode(encoding='UTF-8')
  return json.loads(s)



"""Take a state (key-out session) from the user as JSON, apply the action if it 
exists, look up which taxa are left from the database, and return an HTTP 
response with the new JSON state."""
@csrf_exempt
def updatestate(request):
  
  instate = loadstateJSON(request)
  
  state = None
  try:
    state = keylogic.KeyState(int(instate.get('keyID')))
  except (ValueError, TypeError):
    return HttpResponse('keyID is required and must be an integer.', status=400)
  
  try:
    state.answers = {int(k): v for (k,v) in instate.get('useranswers').items()}
  except ValueError:
    return HttpResponse('Question ID\'s must be integers (or strings parsable into integers)', status=400)
  except AttributeError:
    pass # no 'useranswers' was provided (probably), do nothing
  
  # apply action (eg. the user answered a question)
  if instate.get('action'):
    try:
      action = instate['action']
      if action[0] == 'answer':
        state.answer(int(action[1]), bool(action[2]))
      elif action[0] == 'removeanswer':
        state.remove(int(action[1]))
    except (IndexError, ValueError):
      return HttpResponse('Bad action.  Valid options are [\'answer\', (integer) questionID, (boolean) value] and [\'removeanswer\', (integer) questionID].', status=400)
  
  # look up remaining and eliminated taxa
  eliminatedtaxa = keylogic.eliminatedtaxa(state)
  remainingtaxa = keylogic.remainingtaxa(state, eliminatedtaxa)

  # package up data into JSON response
  response = HttpResponse()
  s = json.dumps({
    'keyID': state.keyID,
    'useranswers': {str(k): v for k,v in state.answers.items()},  
    'action': [],
    'remainingtaxa': [r.id for r in remainingtaxa],
    'eliminatedtaxa': [e.id for e in eliminatedtaxa],
    })
  print ('response', s)
  response.write(s)
  return response
  


"""Render and return the top-level page for a key"""  
@csrf_exempt
def keyview(request, keyID):
  try:
    key = Key.objects.get(pk=int(keyID))
  except (ValueError, ObjectDoesNotExist):
    raise Http404
  
  return render(request, 'key/keyview.html', {'key':key})
  
