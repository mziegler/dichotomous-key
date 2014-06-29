import json

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

import key.keylogic as keylogic
from key.models import Key

# Create your views here.

"""Parse JSON out from the POST request body, applying the action if there is one,
 into a KeyState object"""
def getstate(request):
  #data = json.loads(request.body)
  s = request.body.decode(encoding='UTF-8')
  data = json.loads(s)
  return data
  #TODO create KeyState
  
@csrf_exempt
def updatestate(request):
  #state = getstate(request)
  #return getstate(request)
  #raise Http404
  return HttpResponse(repr(getstate(request)))

"""Render and return the top-level page for a key"""  
@csrf_exempt
def keyview(request, keyID):
  try:
    key = Key.objects.get(pk=int(keyID))
  except (ValueError, ObjectDoesNotExist):
    raise Http404
  
  return render(request, 'key/keyview.html', {'key':key})
  
