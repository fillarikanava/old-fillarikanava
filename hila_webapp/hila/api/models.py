from django.db import models
from django.contrib.auth.models import User, Group
from hila.public.report.models import Theme

class Apikey(models.Model):
    # We'd better store the contact information of the API key's owner
    owner= models.CharField(max_length=30)

    owner_user = models.ForeignKey(User,blank=True)
    owner_email = models.CharField(max_length=30,blank=True)
    owner_phone = models.CharField(max_length=30,blank=True)

    # For checking host later
    host = models.CharField(max_length=30)

    # The real magic:
    key = models.CharField(max_length=30)

    # If a keyword ("theme") is appended into messages left through API:
    associated_tag = models.CharField(max_length=30, blank=True)

    # If the messages left through this api are part of some theme:
    theme = models.ForeignKey(Theme, blank=True)

    # Default user to use for messages left through API:
    default_user = models.CharField(max_length=30,blank=True)

    allow_issue_creation = models.BooleanField()
    allow_commenting = models.BooleanField()
    allow_fileupload = models.BooleanField()




    def __unicode__(self):
        return self.owner+"/"+self.host