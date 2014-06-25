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
  

"""Returns a queryset of the taxa that haven't been eliminated yet."""  
def remainingtaxa(keysession):
  taxa = Taxon.objects.filter(key=keysession.keyID)
  
  # for each question that the user has entered, eliminate all of the taxa
  # that have answers to that question different than what the user provided.
  # (If we don't know the answer to a question for a taxon, don't eliminate
  # that question.)
  for (question, answer) in keysession.answers.items():
    taxa = taxa.exclude(question_taxon__question__id=question,
      question_taxon__answer=answer)
      
  return taxa
    

"""Returns a queryset of the taxa that have been eliminated.  Optionally 
supply the remaining taxa, so we don't have to compute it twice."""
def eliminatedtaxa(keysession, remainingtaxa=None):
  
  taxa = Taxon.objects.filter(key=keysession.keyID)
  _remainingtaxa = remainingtaxa or remainingtaxa(keysession)
  
  return taxa.exclude(pk__in=_remainingtaxa)
  
  
