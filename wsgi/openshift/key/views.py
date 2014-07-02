import json

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt

import key.keylogic as keylogic
from key.models import Key, Question, Taxon



"""Parse JSON out from the POST request body"""
def loadstateJSON(request):
  s = request.body.decode(encoding='UTF-8')
  return json.loads(s)
  


def loadstate(request, parsedJSON=None):
  instate = parsedJSON or loadstateJSON(request)
  
  state = None
  try:
    state = keylogic.KeyState(int(instate.get('keyID')))
  except (ValueError, TypeError):
    raise ValidationError('keyID is required and must be an integer.')
    
  try:
    state.answers = {int(k): v for (k,v) in instate.get('useranswers').items()}
  except ValueError:
    raise ValidationError('Question ID\'s must be integers (or strings parsable into integers)')
  except AttributeError:
    pass # no 'useranswers' was provided (probably), do nothing
    
  state.remainingtaxa = instate.get('remainingtaxa', [])
  state.eliminatedtaxa = instate.get('eliminatedtaxa', [])
    
  return state
    

"""Take a state (key-out session) from the user as JSON, apply the action if it 
exists, look up which taxa are left from the database, and return an HTTP 
response with the new JSON state."""
@csrf_exempt
def updatestate(request):
  
  
  instate = loadstateJSON(request)
  #state = None
  try:
    state = loadstate(request, instate)
  except ValidationError as err:
    return HttpResponse(err.message, status=400)
  
  
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
  
  # suggest a question
  suggestedquestion = keylogic.suggestquestion(state)

  # package up data into JSON response
  response = HttpResponse()
  s = json.dumps({
    'keyID': state.keyID,
    'useranswers': {str(k): v for k,v in state.answers.items()},  
    'action': [],
    'remainingtaxa': [r.id for r in remainingtaxa],
    'eliminatedtaxa': [e.id for e in eliminatedtaxa],
    'suggestedquestion': suggestedquestion,
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
    return HttpResponse("Can't find a key with this keyID!")
  
  return render(request, 'key/keyview.html', {'key':key})
  
  

"""Lists the questions in the key, as well as which questions the user has
already answered."""
@csrf_exempt
def questionlist(request):
  state = loadstate(request)
  questions = keylogic.allquestions(state)
  return render(request, 'key/questionlist.html', {'questions': questions})


"""Show a question"""
@csrf_exempt
def questionview(request, questionID):
  try:
    state = loadstate(request)
  except ValidationError as err:
    return HttpResponse(err.message, status=400)
  
  # get the question from the database
  try:
    question = Question.objects.get(pk=int(questionID))
  except (ValueError, ObjectDoesNotExist):
    return HttpResponse("Can't find a question for this ID!")
  
  # see if the user has already answered the question
  if question.id in state.answers:
    question.hasuseranswer = True
    question.useranswer = state.answers[question.id]
  else:
    question.hasuseranswer = False
    
  return render(request, 'key/questionview.html', {'question': question})
  

"""Show a list of remaining and eliminated taxa"""
@csrf_exempt
def taxalist(request):
  try:
    state = loadstate(request)
  except ValidationError as err:
    return HttpResponse(err.message, status=400)
    
  remainingtaxa = Taxon.objects.filter(id__in=state.remainingtaxa)
  eliminatedtaxa = Taxon.objects.filter(id__in=state.eliminatedtaxa)
  
  return render(request, 'key/taxalist.html', 
    {'remainingtaxa': remainingtaxa, 'eliminatedtaxa': eliminatedtaxa})
  
