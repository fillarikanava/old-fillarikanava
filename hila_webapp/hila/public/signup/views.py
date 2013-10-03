from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from hila.public.signup.forms import RegistrationFormUniqueEmail, ActivationRequestForm
from hila.public.signup.models import RegistrationProfile


def activate(request, activation_key, template_name='activate.html', extra_context=None):
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name, { 'account': account, 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS }, context_instance=context)

def activation_request(request, success_url=None, form_class=ActivationRequestForm, template_name='activation_request.html', extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(success_url or reverse('activation_request_sent'))
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    return render_to_response(template_name, { 'form': form }, context_instance=context)
    
def activation_request_sent(request, template_name='activation_request_sent.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))
    
    
def register(request, success_url=None, form_class=RegistrationFormUniqueEmail, template_name='registration_form.html', extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save()
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponseRedirect(success_url or reverse('registration_complete'))
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name, { 'form': form }, context_instance=context)

def xd_receiver(request):
    return render_to_response('xd_receiver.html')
