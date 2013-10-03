# Copyright 2008-2009 Brian Boyer, Ryan Mark, Angela Nitzke, Joshua Pollock,
# Stuart Tiffen, Kayla Webley and the Medill School of Journalism, Northwestern
# University.
#
# This file is part of django-facebookconnect.
#
# django-facebookconnect is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-facebookconnect is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with django-facebookconnect.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sha, random

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.conf import settings

from hila.facebookconnect.models import FacebookProfile

debugging = True

def facebook_login(request):
    if request.method == "POST":
        logging.debug("FBC: OK logging in...")
        if request.POST.get('next',False) and request.POST['next']:
            next = request.POST['next']
        else:
            next = getattr(settings,'LOGIN_REDIRECT_URL','/')
        user = authenticate(request=request)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    print "=== Trying to get screenname"
                    print "=== screenname is: "+ str(user.first_name)
                    #REST_SERVER = 'http://api.facebook.com/restserver.php'
                    
                    #print "fb_username is: " +str(request.facebook.)
                    #if len(str(user.first_name)) < 1:
                    #    import roundup_utils
                except:
                    print "Did not work"
                # Redirect to a success page.
                logging.debug("FBC: Redirecting to %s" % next)
                return HttpResponseRedirect(next)
            else:
                logging.debug("FBC: This account is disabled.")
                raise FacebookAuthError('This account is disabled.')
        elif request.facebook.uid:
            #we have to set this user up
            logging.debug("FBC: Redirecting to setup")
            return HttpResponseRedirect(reverse('facebook_setup')+"?next=%s" % next)
    
    logging.debug("FBC: Got redirected here")
    url = reverse('login')
    if request.GET.get('next',False):
        url += "?next=%s" % request.GET['next']
    return HttpResponseRedirect(url)

def facebook_logout(request):
    logout(request)
    if getattr(request,'facebook',False):
        request.facebook.session_key = None
        request.facebook.uid = None
    return HttpResponseRedirect(getattr(settings,'LOGOUT_REDIRECT_URL','/'))
    
def setup(request):
    if debugging:
        from datetime import datetime
        print str(datetime.now()) +" debugging facebook problems"
    if not request.facebook.uid:
        if debugging:
            print "not request.facebook.uid, returning"

        return HttpResponseRedirect(reverse('login')+"?next="+request.GET.get('next',''))
    
    if request.method == "POST":
        if debugging:
            print "request method was post"

        if request.POST.get('next',False) and request.POST['next']:
            next = request.POST['next']
        else:
            next = getattr(settings,'LOGIN_REDIRECT_URL','/')

        try:
            profile = FacebookProfile.objects.get(pk=request.facebook.uid)
            if debugging:
                print "Found old profile for "+request.facebook.uid
        except:
            profile = FacebookProfile(facebook_id=request.facebook.uid)
            if debugging:
                print "Created new profile for " + request.facebook.uid
        if debugging:
            print "Profile for uid " +str(request.facebook.uid) + ": " + str (profile)

        if request.POST.get('facebook_only',False):
            if debugging:
                print "request post facebook only is false"
            try:
                user = User.objects.get(username__exact=request.facebook.uid)                
            except:
                user = User(username=request.facebook.uid,
                            password=sha.new(str(random.random())).hexdigest()[:8],
                            email=profile.email)
            user.save()

            if debugging:
                print "saved user " +str(user)

            profile.user = user
            profile.save()

            logging.info("FBC: Added user and profile for %s!" % request.facebook.uid)
            user = authenticate(request=request)

            if debugging:
                print "authenticated user " +str(user)

            login(request, user)

            if debugging:
                print "Logged in user, returning"

            return HttpResponseRedirect(next)

        if debugging:
            print "request facebook only true"

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            if debugging:
                print "Authentication form valid"

            user = form.get_user()

            if debugging:
                print "get user from form"

            logging.debug("FBC: Trying to setup FB: %s, %s" % (user,profile))
            if user is not None and user.is_active:
                if debugging:
                    print "User exists"

                profile.user = user
                profile.save()
                logging.info("FBC: Attached facebook profile %s to user %s!" % (profile.facebook_id,user))
                login(request, user)
                if debugging:
                    print "Attached profile, returning"

                return HttpResponseRedirect(next)
        else:
            if debugging:
                print "Form was not valid, doing something with a user"

            user = User()
            user.facebook_profile = profile
    
    elif request.user.is_authenticated():
        if debugging:
            print "User was already authenticated, so do something and return"

        profile = FacebookProfile(facebook_id=request.facebook.uid)
        profile.user = request.user
        profile.save()
        logging.info("FBC: Attached facebook profile %s to user %s!" % (profile.facebook_id,user))
        return HttpResponseRedirect(next)
    
    else:
        if debugging:
            print "No post data, no authentication done, doing a user and then what?"

        user = User()
        user.facebook_profile = FacebookProfile(facebook_id=request.facebook.uid)

#        print "I added user.save() here:"
#        user.save()

        next = request.GET.get('next','')
        form = AuthenticationForm(request)
        if debugging:
            print "Adding authentication form here"

    if debugging:
        print "Returning form with user: >"+str(user) + "< form: "+ str(form) + " next: "+str(next)


    return render_to_response(
        'facebook/setup.html',
        {"user":user,
         "form":form,
         "next":next},
        context_instance=RequestContext(request))

class FacebookAuthError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
