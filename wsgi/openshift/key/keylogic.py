from key.models import Key, Taxon, Question, Question_Taxon

"""A finite state machine for traversing a key"""
class KeyState:

  """Initialize the key state from an existing state, or start a fresh state.
  self.keyID is matches a key ID in the database.
  self.answers is a dictionary of questionID-answer pairs that the user has supplied."""
  def __init__(self, keyID, answers=None):
    self.keyID = keyID
    
    if answers:
      self.answers = answers
    else:
      self.answers = dict() #empty dictionary


  """The user answers a question in the key state"""
  def answer(self, questionID, answer):
    self.answers[questionID] = answer
    return self
  

  """Un-answers a question in the key state"""  
  def remove(self, questionID):
    try:
      del self.answers[questionID]
    except KeyError:
      pass
    return self
  

"""Get all questions (a QuerySet) for a key state.  The question objects will
have 2 extra attributes, 'hasuseranswer' and 'useranswer', with the user's 
answers to the questions."""
def allquestions(keystate):
  # get all the questions for this key
  questions = Question.objects.filter(key=keystate.keyID)
  
  # attach the users' responses to the questions
  for q in questions:
    if q.id in keystate.answers:
      q.hasuseranswer = True
      q.useranswer = keystate.answers[q.id]
    else:
      q.hasuseranswer = False 
      q.useranswer = None # None if the user hasn't answered the question
      
  return questions
    


"""Suggest a question for the user to answer.  Possibly change this later
to use decision trees and calculate information gain for each question.
Return -1 if there are no questions left."""    
def suggestquestion(keystate):
  q = Question.objects.filter(key=keystate.keyID)\
    .exclude(id__in=keystate.answers.keys())[0]
  if q:
    return q.id
  else:
    return -1
  


"""Returns a queryset of the taxa that have been eliminated for this key
state."""
def eliminatedtaxa(keystate):
  
  keytaxa = Taxon.objects.filter(key=keystate.keyID) # taxa for this key
  taxa = Taxon.objects.none() # empty QuerySet
  
  # union of taxa that have an answer that differs from a user-supplied answer
  for (question, answer) in keystate.answers.items():
    taxa = taxa | keytaxa.filter(
      question_taxon__question=question,
      question_taxon__answer=not answer)
      
  return taxa
  

"""Returns a queryset of the taxa that are remaining for this key state. 
Optionally supply the eliminated taxa, so we don't have to compute it twice."""
def remainingtaxa(keystate, eliminated=None):
  _eliminated = eliminated or eliminatedtaxa(keystate)
  return Taxon.objects.filter(key=keystate.keyID).exclude(pk__in=_eliminated)


