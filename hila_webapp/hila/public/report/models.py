from django.db import models
from hila.public.profiles.models import UserProfile as user
import multilingual
from datetime import datetime
#
#class report(models.Model):
#    title = models.CharField(max_length=160)
#    comments = models.ManyToOneRel(comment)
##    files = models.ManyToOneRel(file)
#    nosy = models.ManyToOneRel(user)
##   assignedTo = models.ManyToOneRel(user)
#    priority = models.IntegerField()
#    status = models.IntegerField()
#    places = models.ManyToOneRel(place)
#    organisation = models.ManyToOneRel(organisation)
#    superseders = models.ManyToOneRel(report)
#    continuation = models.OneToOneRel(report)
#
#class comment(models.Model):
#    dummy = 0
#
#class place(models.Model):
#    lng=models.CharField(max_length=16)
#    lat=models.CharField(max_length=16)
#    address=models.CharField(max_length=64)
#    postalcode=models.CharField(max_length=16)
#    city=models.CharField(max_length=64)
#    country=models.CharField(max_length=64)
#    streetview=models.CharField(max_length=64)
#
#class organisation(models.Model):
#    dummy = 1



class Theme(models.Model):

    name = models.CharField(max_length=30)
    associated_tag = models.CharField(max_length=30, blank=True)

    searchable = models.BooleanField(default=True)


    custom_css = models.TextField(max_length=500,blank=True)
    custom_javascript = models.TextField(max_length=500,blank=True)


    allow_issue_creation_start = models.DateTimeField(blank=True, null=True)
    allow_issue_creation_stop = models.DateTimeField(blank=True, null=True)

    allow_commenting_start = models.DateTimeField(blank=True, null=True)
    allow_commenting_stop = models.DateTimeField(blank=True, null=True)


    allow_api_import = models.BooleanField()


    class Translation(multilingual.Translation):
        description = models.CharField(max_length=100,blank=True)

        custom_ingress_short = models.TextField(max_length=500,blank=True)
        custom_ingress_long = models.TextField(max_length=500,blank=True)
        custom_logo = models.CharField(max_length=150,blank=True)
        custom_create_logo = models.CharField(max_length=150,blank=True)




    def __unicode__(self):
        return self.name

    def allow_issue_creation(self):
        if not self.allow_issue_creation_start or not self.allow_issue_creation_stop:
            return True
        if self.allow_issue_creation_start < datetime.now() < self.allow_issue_creation_stop:
            return True
        return False

    def allow_commenting(self):
        if not self.allow_commenting_start or not self.allow_commenting_stop:
            return True
        if self.allow_commenting_start < datetime.now() < self.allow_commenting_stop:
            return True
        return False

