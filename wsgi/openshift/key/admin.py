from django.contrib import admin
from key.models import Key, Taxon, Question, Question_Taxon

# Register your models here.
admin.site.register(Key)
admin.site.register(Taxon)
admin.site.register(Question)
admin.site.register(Question_Taxon)
