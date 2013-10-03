from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.http import HttpResponseRedirect, HttpResponseServerError, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from hila.public.report.forms import ReportForm
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from hila import roundup_utils
import hila.roundup_utils 
from roundup.date import Date
from util import render_with_default
import re
import forms, datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from hila.api import issue_to_dict
from hila.public.profiles.models import UserProfile
from util.misc_utils import get_tag_decorations
from datetime import datetime
from hila.public.report.models import Theme

AUTHORIZED_GROUPS = ['HILA', 'Kaupunkisuunnitteluvirasto']

def index(request):
    return view(request, None)

def view(request, report_id, tag=None):


    try:
        roundup_utils.find_issue(report_id)
    except:
        raise Http404
    
    if request.method == 'POST': #and not roundup_utils.is_anon_userid(roundup_utils.get_user_id(request)):
        #print "report_id: " + report_id
        form_comment = forms.CommentForm(request.POST)
        if not form_comment.is_valid():
            return HttpResponseServerError(unicode(form.errors))

        form_file = forms.FileUploadForm(request.POST, request.FILES)
        if not form_file.is_valid():
            return HttpResponseServerError(unicode(form.errors))

        comment = form_comment.cleaned_data['comment']
        if form_comment.is_valid():
            new_msg_id = roundup_utils.create_message(author=roundup_utils.get_user_id(request),
                                         content=comment.encode('utf-8'), 
                                         date=Date(), 
                                         issue_id=report_id)

            print str(datetime.now()) + " New message id: " + str(new_msg_id)
            form_geo = forms.GeodataForm(request.POST)
            if form_geo.is_valid():
                            
                address = form_geo.cleaned_data['issueaddress']
                postal = form_geo.cleaned_data['issuepostal']
                lng = form_geo.cleaned_data['issuelng']
                lat = form_geo.cleaned_data['issuelat']
                city = form_geo.cleaned_data['issuecity']
                country = form_geo.cleaned_data['issuecountry']


                if postal is None or len(postal) < 1:
                    postal = ''
                if address is None or len(address) < 1:
                    address = postal
        
                if len(country)>0 and len(lng)>0 and len(lat)>0 and len(city)>0: 
                    print str(datetime.now()) + " Trying to create new place:"
                    place = roundup_utils.create_place(lng=lng,
                        lat=lat,
                        address=address.encode('utf-8'),
                        postalcode=postal,
                        city=city.encode('utf-8'),
                        country=country.encode('utf-8'),
                        message_id=new_msg_id)

                elif len(lng)>0 and len(lat)>0:
                    print str(datetime.now()) + " report/views.py: Country and city somehow not defined!"
                    place = roundup_utils.create_place(lng=lng,
                        lat=lat,
                        address=address.encode('utf-8'),
                        postalcode=postal,
                        city="Helsinki",
                        country="Finland",
                        message_id=new_msg_id) 
            else:
                print  str(datetime.now()) +  " form geo is not valid!"
                print str(datetime.now()) + " address "+ str(address) + "/postal " + str(postal) + "/lng " + \
                    str(lng) + "/lat "+ str(lat) + "/city "+str(city)+ "/country "+country


            if form_file.is_valid():
                uploaded_file = request.FILES.get('file', None)
                if uploaded_file is not None:
                # Dangerous... Should be a limit to upload size!
                    uploaded_file = request.FILES['file']
                    if uploaded_file:
                        file_id = roundup_utils.create_file(content=uploaded_file.read(),
                                                        name=uploaded_file.name,
                                                        message_id = new_msg_id)
        
    
    db = roundup_utils.db()


    history  = []
    for history_item in db.issue.history(report_id):

        #The returned list contains tuples of the form
        #
        #    (nodeid, date, tag, action, params)
        #
        #'date' is a Timestamp object specifying the time of the change and
        #'tag' is the journaltag specified when the database was opened.
        
        history.append(str(history_item[1]) + " " + str(history_item[3])+ " " + str(history_item[4]))
    
    search_id = int(report_id) +1
    while search_id < int(report_id) +10 and not db.issue.hasnode(str( search_id )):
        search_id += 1
        
#    if search_id < int(report_id) +10:
#        next_issue = issue_to_dict(None, issue_id=str(search_id))
#    else:    
    next_issue = {}
    
    search_id = int(report_id) -1
    while search_id > 0 and not db.issue.hasnode(str( search_id )):
        search_id -= 1
        
    if search_id > 0:
        prev_issue = issue_to_dict(None, issue_id=str(search_id))
    else:
        prev_issue = { }
    
    return render_with_default(
        {'issue' : issue_to_dict(None, report_id),
         'form_geo' : forms.GeodataForm(),
         'form_comment' : forms.CommentForm(),
         'form_file' : forms.FileUploadForm(),
         'history' : history,
         'next' : next_issue,
         'prev' : prev_issue,
         'decorations': get_tag_decorations(tag)
         #         'mapbounds' : mapbounds,
        }, 
        RequestContext(request))



def create(request, tag = None):
    print str(datetime.now()) + "Creating new! Tag: "+str(tag)
    values = {}
    if request.method == 'POST':

        #if request.get("")
        form_captcha = forms.CaptchaForm(request.POST)
        form_main = forms.ReportForm(request.POST)
        form_details = forms.DetailsForm(request.POST)
        form_keywords = forms.KeywordsForm(request.POST)
        form_user = forms.UserdataForm(request.POST)
        form_geo = forms.GeodataForm(request.POST)
        form_file = forms.FileUploadForm(request.POST, request.FILES)

        if form_main.is_valid() and form_geo.is_valid():

            title = form_main.cleaned_data['message']
            
            if form_details.is_valid():            
                message = form_details.cleaned_data['details']
            
            if form_keywords.is_valid():
                keywords = form_keywords.cleaned_data['keywords']
            
            if request.user.is_authenticated():
                form_user.fields['userfullname'].widget.attrs['readonly'] = 'readonly'
                userid = request.user.id
            


                # maybe send an email to user after issue creation?
                # recipients.append(useremail)
                # from django.core.mail import send_mail
                # send_mail(title, message, "mailbot@openfeedback.org", recipients)
    
#                if request.user.is_authenticated():
#                    userid = request.user.id
#                else:
#                    userid = db.user.get_user_id(request)

            userid = roundup_utils.get_user_id(request)

            if form_captcha.is_valid() or not roundup_utils.is_anon_userid(userid):


                keyword_array = re.split(r'[, ;:]', keywords)
                issue_keywords = []
                for keyword in keyword_array:
                    if len(keyword) >0 :
                        issue_keywords.append(keyword.encode('utf-8'))
                id=roundup_utils.create_issue(title=title.encode('utf-8'),
                                              keywords=issue_keywords,
                                              author=roundup_utils.get_user_id(request))

                if message:
                    msg_id = roundup_utils.create_message(author=userid,
                                           content=message.encode('utf-8'),
                                           date=Date(),
                                           issue_id = id)

                if form_geo.is_valid():
                    address = form_geo.cleaned_data['issueaddress']
                    postal = form_geo.cleaned_data['issuepostal']
                    lng = form_geo.cleaned_data['issuelng']
                    lat = form_geo.cleaned_data['issuelat']
                    city = form_geo.cleaned_data['issuecity']
                    country = form_geo.cleaned_data['issuecountry']

                    if postal is None or len(postal) < 1:
                        postal = ''
                    if address is None or len(address) < 1:
                        address = postal

                    if len(country)>0 and len(lng)>0 and len(lat)>0 and len(city)>0:
                        try:
                            print str(datetime.now()) + "Adding place:" + str(country) + "/" + str(lng)+"/" + str( city) + "/" + str(address)
                        except:
                            print str(datetime.now()) + "could not print good map location"
                        place_id = roundup_utils.create_place(lng=lng,
                            lat=lat,
                            address=address.encode('utf-8'),
                            postalcode=postal,
                            city=city.encode('utf-8'),
                            country=country.encode('utf-8'),
                            issue_id=id )
                    else:
                        try:
                            print str(datetime.now()) + "Place attributes bad:" + str(country) + "/" + str(lng)+"/" + str( city) + "/" + str(address)
                        except:
                            print str(datetime.now()) + "could not print bad map location"

                if form_file.is_valid():
                    # Dangerous... Should be a limit to upload size!
                    uploaded_file = request.FILES.get('file', None)
                    if uploaded_file is not None:
                        print str(uploaded_file) + " "+ str(uploaded_file.size)
                        if uploaded_file:
                            file_id = roundup_utils.create_file(content=uploaded_file.read(),
                                                            name=uploaded_file.name,
                                                            issue_id = id)

                if tag:
                    print "=====================Tag so returning tagged_report_view"
                    return HttpResponseRedirect(reverse('tagged_report_view', args=[tag,id]))
                else:
                    print "=====================No tag so returning report_view"
                    return HttpResponseRedirect(reverse('report_view', args=[id]))
            else:

                print str(datetime.now()) + "Captha valid? "+ str(form_captcha.is_valid())

                values = {'form_main': form_main, 'form_details': form_details,
                                                    'form_geo': form_geo,  'form_user': form_user,
                                                    'form_file': form_file,'form_keywords': form_keywords }

                if tag:
                    if tag == "talvikysely":
                        print str(datetime.now()) + "adding form_captcha!"
                        values.update( { 'form_captcha': forms.CaptchaForm(request.POST)}, )


                    values.update( { 'decorations': get_tag_decorations(tag)}, )
                    print "str(datetime.now()) + =====================Bad form so returning something"
                    return render_to_response('create.html', values, RequestContext(request))
                print "str(datetime.now()) + =====================Bad form so returning default"
                return render_to_response('create.html', values, RequestContext(request))
    else:

        form_captcha = None
        if tag == "talvikysely":
            print str(datetime.now()) + "adding form_captcha!"
            form_captcha = forms.CaptchaForm(request.POST)

        form_details = forms.DetailsForm()
        form_keywords = forms.KeywordsForm(initial={'keywords':tag})
        form_main = forms.ReportForm()
        form_geo = forms.GeodataForm()
        form_file = forms.FileUploadForm()


        if request.user.is_authenticated():
            userfullname = request.user.get_full_name()
            form_user = forms.UserdataForm(initial={'userfullname': userfullname})
            form_user.fields['userfullname'].widget.attrs['readonly'] = 'readonly'
            
        else:
            form_user = forms.UserdataForm()
        
        values = {'form_captcha': form_captcha, 'form_main': form_main, 'form_details': form_details,
                                                'form_geo': form_geo,  'form_user': form_user,
                                                'form_file': form_file,
                                                'form_keywords': form_keywords  }


        if request.GET.has_key(u'lat') and request.GET.has_key(u'lng'):
            print "Adding: " + str(request.GET)
            values.update( { 'lat': request.GET[u'lat'], 'lng': request.GET[u'lng'] })

    values.update( { 'decorations': get_tag_decorations(tag)} )

    return render_to_response('create.html', values, RequestContext(request))

def edit(request, report_id, tag = None):
    try:
        profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('report_view', args=[report_id]))
    issue = roundup_utils.issue_to_dict(None, issue_id=str(report_id))
    if issue['options']['author_id'] == profile.roundup_id or bool(request.user.groups.filter(name__in=AUTHORIZED_GROUPS).values('name')):
        if request.method == 'POST':
            form_main = ReportForm(request.POST)
            if form_main.is_valid():
                roundup_utils.update_issue(issue_id=report_id, title=form_main.cleaned_data['message'])
                return HttpResponseRedirect(reverse('report_view', args=[report_id]))
        else:
            form_main = ReportForm(initial={'message':issue['title']})
            return render_to_response('edit.html', {'form_main': form_main, 'report_id': issue['options']['id'] }, RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('report_view', args=[report_id]))

def delete(request, report_id,tag=None):
    try:
        profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('report_view', args=[report_id]))
    issue = roundup_utils.issue_to_dict(None, issue_id=str(report_id))
    if issue['options']['author_id'] == profile.roundup_id or bool(request.user.groups.filter(name__in=AUTHORIZED_GROUPS).values('name')):
        if request.method == 'POST':
            roundup_utils.retire_issue(report_id)
            return HttpResponseRedirect(reverse('public_front'))
        else:
            return HttpResponseRedirect(reverse('report_view', args=[report_id]))
    else:
        return HttpResponseRedirect(reverse('report_view', args=[report_id]))

@require_POST
@commit_on_success
def comment(request, report_id,tag=None):
    print str(datetime.now()) + "adding a comment to report nr. "+report_id
    
    try:
        profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('report_view', args=[report_id]))
    
#    issue = node_or_404(db.issue, report_id)
    form = forms.CommentForm(request.POST)
    if not form.is_valid():
        return HttpResponseServerError(unicode(form.errors))

    roundup_utils.create_message(author=roundup_utils.get_user_id(request),
                                 content=form.cleaned_data['comment'].encode('utf-8'), 
                                 date=Date(), 
                                 issue_id = report_id)

    return HttpResponseRedirect(reverse('report_view', args=[report_id]))


def comment_edit(request, report_id, comment_id,tag=None):
    try:
        profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('report_view', args=[report_id]))
    message = roundup_utils.message_to_dict(None, id=str(comment_id))
    pass

def search(request):

    form_search = forms.SearchForm()

    values = {'form_search': form_search}

    if request.GET.has_key(u'terms'):
        values.update( { 'search_terms': request.GET[u'terms'] })

    
    return render_to_response('search.html', values, RequestContext(request))
    
