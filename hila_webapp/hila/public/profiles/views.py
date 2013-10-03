from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list

from hila.public.profiles import utils
from hila.public.profiles.forms import UserProfileForm

from hila import roundup_utils


def create_profile(request, form_class=UserProfileForm, success_url=None, template_name='create_profile.html', extra_context=None):
    try:
        profile_obj = request.user.get_profile()
        return HttpResponseRedirect(reverse('profiles_edit_profile'))
    except ObjectDoesNotExist:
        pass
    
    if success_url is None:
        success_url = reverse('user_profile', kwargs={ 'username': request.user.username })
    if form_class is None:
        form_class = utils.get_profile_form()
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            profile_obj = form.save(commit=False, userobj=request.user)
            profile_obj.user = request.user
            profile_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)
create_profile = login_required(create_profile)

def edit_profile(request, form_class=UserProfileForm, success_url=None, template_name='edit_profile.html', extra_context=None):
    try:
        profile_obj = request.user.get_profile()
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('profiles_create_profile'))
    
    if success_url is None:
        success_url = reverse('user_profile', kwargs={ 'username': request.user.username })
    if form_class is None:
        form_class = utils.get_profile_form()
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save(userobj=request.user)
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(instance=profile_obj)
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name, { 'form': form, 'profile': profile_obj, }, context_instance=context)
edit_profile = login_required(edit_profile)

def anonymous_detail(request, public_profile_field=None, template_name='profile_detail.html', extra_context=None):

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              { 'profile': None,
                                'issues': None,
                                'messages': None },
                              context_instance=context)

def profile_detail(request, username, public_profile_field=None, template_name='profile_detail.html', extra_context=None):
    user = get_object_or_404(User, username=username)
    try:
        profile_obj = user.get_profile()
    except ObjectDoesNotExist:
        raise Http404
    if public_profile_field is not None and \
       not getattr(profile_obj, public_profile_field):
        profile_obj = None
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'profile': profile_obj,
                                'issues': roundup_utils.get_issues_by_user(username=username),
                                'messages': roundup_utils.get_messages_by_user(username=username) },
                              context_instance=context)

def profile_list(request, public_profile_field=None, template_name='profile_list.html', **kwargs):
    profile_model = utils.get_profile_model()
    queryset = profile_model._default_manager.all()
    if public_profile_field is not None:
        queryset = queryset.filter(**{ public_profile_field: True })
    kwargs['queryset'] = queryset
    return object_list(request, template_name=template_name, **kwargs)