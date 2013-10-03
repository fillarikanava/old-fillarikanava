'''
Created on 31.3.2009

@author: jsa
'''

from django.template.context import RequestContext
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from util import render_with_default
from hila import roundup_utils
from hila.public.registration.forms import RegistrationForm

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            roundup_user = roundup_utils.getnode(new_user)
            # Sign the user in
            auth_user = authenticate(username=roundup_user.username, password=roundup_user.password)
            if auth_user:
                login(request, auth_user)
            return HttpResponseRedirect(reverse('signup_complete'))
    else:
        form = RegistrationForm()
    
    return render_to_response('registration.html', {'form' : form}, context_instance=RequestContext(request))
#    raise NotImplementedError

def activate(request, activation_key):
    raise NotImplementedError

def profile(request):
    return render_with_default({}, RequestContext(request))

def logout_view(request):
    logout(request)

def xd_receiver(request):
    return render_to_response('xd_receiver.html')

def fb_connect(request):
    return render_to_response('fb_connect.html')


