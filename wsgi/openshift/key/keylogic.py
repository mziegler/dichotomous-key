from key.models import Key, Taxon, Question, Question_Taxon

"""A finite state machine for traversing a key"""
class KeySession:

  """Initialize the key session from an existing session, or start a fresh session.
  self.keyID is matches a key ID in the database.
  self.answers is a dictionary of questionID-answer pairs that the user has supplied."""
  def __init__(self, keyID, answers=None):
    self.keyID = keyID
    
    if answers:
      self.answers = answers
    else:
      self.answers = dict() #empty dictionary


  """The user answers a question in the key session"""
  def answer(self, questionID, answer):
    self.answers[questionID] = answer
    return self
  

  """Un-answers a question in the key-session"""  
  def remove(self, questionID):
    try:
      del self.answers[questionID]
    except KeyError:
      pass
    return self
  

"""Get all questions (a QuerySet) for a key session.  The question objects will
have 2 extra attributes, 'hasuseranswer' and 'useranswer', with the user's 
answers to the questions."""
def allquestions(keysession):
  # get all the questions for this key
  questions = Question.objects.filter(key=keysession.keyID)
  
  # attach the users' responses to the questions
  for q in questions:
    if q.id in keysession.answers:
      q.hasuseranswer = True
      q.useranswer = keysession.answers[q.id]
    else:
      q.hasuseranswer = False 
      q.useranswer = None # None if the user hasn't answered the question
      
  return questions
    

"""Returns a queryset of the taxa that have been eliminated for this key
session."""
def eliminatedtaxa(keysession):
  
  keytaxa = Taxon.objects.filter(key=keysession.keyID) # taxa for this key
  taxa = Taxon.objects.none() # empty QuerySet
  
  # union of taxa that have an answer that differs from a user-supplied answer
  for (question, answer) in keysession.answers.items():
    taxa = taxa | keytaxa.filter(
      question_taxon__question=question,
      question_taxon__answer=not answer)
      
  return taxa
  

"""Returns a queryset of the taxa that are remaining for this key session. 
Optionally supply the eliminated taxa, so we don't have to compute it twice."""
def remainingtaxa(keysession, eliminated=None):
  _eliminated = eliminated or eliminatedtaxa(keysession)
  return Taxon.objects.filter(key=keysession.keyID).exclude(pk__in=_eliminated)


