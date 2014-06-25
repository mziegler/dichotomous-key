from django.db import models

class Key(models.Model):
  name = models.CharField(max_length=128)
  description = models.TextField()    
  # TODO link to user and/or group? Create an auth group for each key?
  # last-modified timestamp?
  
  def __str__(self):
    return 'Key {0}: {1}'.format(self.id, self.name)
 
 
class Taxon(models.Model):
  key = models.ForeignKey(Key)
  name = models.CharField(max_length=256)
  TOLwebID = models.PositiveIntegerField(null=True) #optional
  description = models.TextField()
  # timestamp?
  # user? 
  
  def __str__(self):
    return 'Taxon {0}: {1}'.format(self.id, self.name)
 
 
class Question(models.Model):
  key = models.ForeignKey(Key)
  shortname = models.CharField(max_length=40)
  text = models.TextField()
  taxa = models.ManyToManyField(Taxon, through='Question_Taxon')
  # link to pictures?
  # user?
  # timestamp?
  
  def __str__(self):
    return 'Question {0}: {1}'.format(self.id, self.shortname)
    
  
class Question_Taxon(models.Model):
  question = models.ForeignKey(Question)
  taxon = models.ForeignKey(Taxon)
  answer = models.BooleanField()
  # timestamp?
  # user?
  

