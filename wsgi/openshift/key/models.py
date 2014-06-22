from django.db import models

class Key(models.Model):
  name = models.CharField(max_length=128)
  description = models.TextField()    
  # TODO link to user and/or group? Create an auth group for each key?
  # last-modified timestamp?
 
class Taxon(models.Model):
  key = models.ForeignKey(Key)
  name = models.CharField(max_length=256)
  TOLwebID = models.PositiveIntegerField(null=True) #optional
  description = models.TextField()
  # timestamp?
  # user? 
 
class Question(models.Model):
  key = models.ForeignKey(Key)
  shortname = models.CharField(max_length=40)
  text = models.TextField()
  taxa = models.ManyToManyField(Taxon, through='Question_Taxon')
  # link to pictures?
  # user?
  # timestamp?
  
class Question_Taxon(models.Model):
  question = models.ForeignKey(Question)
  taxon = models.ForeignKey(Taxon)
  answer = models.BooleanField()
  # timestamp?
  # user?
