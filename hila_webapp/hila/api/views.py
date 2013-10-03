# -*- coding: UTF-8 -*-

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.utils.simplejson import dumps
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from hila import roundup_utils
from hila import map_utils
from hila.api import issue_to_dict, issue_to_quick_dict
from util.misc_utils import get_latest_messages, get_popular_messages, get_officer_messages
from util import json_resp
import forms
import logging
import random, re
from math import sqrt, ceil
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import os
from datetime import datetime
import simplejson as json

import adding_through_api


try:
    import xapian
    xapian_avail = True
except ImportError:
    logging.warning('Failed to import xapian, search disabled')
    xapian_avail = False



@json_resp
@require_GET
def search(request):
    db = roundup_utils.db()

    form = forms.SearchForm(request.GET)
    if not form.is_valid():
        return HttpResponseServerError(dumps(form.errors))
    coords = form.cleaned_data.get('coords', None)
    if coords:
        x1, x2, y1, y2 = [int(c) for c in coords.split(',')]
    else:
        x1 = x2 = y1 = y2 = None
    status = form.cleaned_data.get('status', None)
    status_id = status and db.status.filter(None, {'name': status})[0] \
                       or None
    issue_data = []
    # TODO just for testing; use Xapian
    for issue in db.issue.getnodes(db.issue.list()):
        if status_id and str(issue.status) != status_id:
            continue
        issue_data.append(issue_to_dict(issue))
    return HttpResponse(dumps(issue_data))



cluster_thr_for_zoomlevel={3:4000,
                           4:1700,
                           5:1100,
                           6:700,
                           7:600,
                           8:400,
                           9:200,
                           10:90,
                           11:60,
                           12:30,
                           13:15,
                           14:6,
                           15:1,
                           16:1,
                           17:1}




def get_latlng_keywords(strvalue1,strvalue2):
    value1 = float(strvalue1)
    value2 = float(strvalue2)
    
    binborder=float(int(value1*10))/10
    
    border_keywords=[]

    if value2 < value1:
        tmp = value1
        value2 = value1
        value1 = tmp
    
    while binborder <= value2:
        border_keywords.append(str(binborder)+"_"+str(binborder+0.05))
        binborder+=0.05
     
    return border_keywords


@json_resp
def xapian_search(request):

    if not xapian_avail:
        return HttpResponse('{}')

    
    search_string = request.GET.get('keywords', None)
    try:
        search_limit = int(request.GET.get('slimit', str(settings.MAX_MATCHES_SEARCH)))
    except:
        search_limit = settings.MAX_MATCHES_SEARCH
    try:
        view_limit = int(request.GET.get('vlimit', str(settings.MAX_MATCHES_SHOW)))
    except:
        view_limit = settings.MAX_MATCHES_SHOW
    offset = int(request.GET.get('offset', 0))
    search_max_result_length = int(request.GET.get('maxchars', '0'))
    zoomlevel = int(request.GET.get('zoomlevel', 12))
    cluster = float(request.GET.get('cluster', 0))
    details = str(request.GET.get('details', "no"))
    from_date = str(request.GET.get('datefrom', None))
    to_date = str(request.GET.get('dateto', None))


    seqnum= str(request.GET.get('seqnum', 0))

    coords = {
        'x1': float(request.GET.get('x1', 0)),
        'y1': float(request.GET.get('y1', 0)),
        'x2': float(request.GET.get('x2', 0)),
        'y2': float(request.GET.get('y2', 0)),
    }


    statuses = None
    if 'status' in request.GET:
        statuses = [int(status) for status in
                    request.GET.getlist('status')]

    tags = None
    if 'tag' in request.GET:
        tags = [ "_key_"+str(tag) for tag in
                    request.GET.getlist('tag')]
    elif 'no_tags' in request.GET:
        tags = [ "_no_key" ]

    request.session['mapzoomlevel'] = zoomlevel
    request.session['mapcenterlat'] = ( coords['y1'] + coords['y2'] ) / 2
    request.session['mapcenterlng'] = ( coords['x1'] + coords['x2'] ) / 2

    if int(request.GET.get('nosearch', 0)) > 0:
        return HttpResponse('{}')

    
    if from_date is not "None":
        date_array = from_date.split('/')
        if len(date_array) > 2:
            if int(date_array[2]+date_array[1]+date_array[0]) > 20090101:
                request.session['filter_from_date'] = str( date_array[1]+"/"+date_array[0]+"/"+date_array[2] )
            else:
                request.session['filter_from_date'] = "01/01/2009"
        else:
            from_date="01/01/2009"

    if to_date is not "None":
        date_array = to_date.split('/')
        if len(date_array) > 2:
            if int(date_array[2]+date_array[1]+date_array[0]) < int( datetime.now().strftime('%y%m%d')):
                request.session['filter_to_date'] = str( date_array[1]+"/"+date_array[0]+"/"+date_array[2] )
            else:
                request.session['filter_to_date'] = str( datetime.now().strftime('%m/%d/%Y'))
        else:
            to_date=str( datetime.now().strftime('%d/%m/%Y'))

    if search_string:
        request.session['filter_words'] = search_string
    else:
        request.session['filter_words'] =  ''

    returnarray = []
    
    
#    database = xapian.Database(settings.XAPIAN_MSG_DATABASE_HOME)
    database = xapian.Database( os.path.join(settings.TRACKER_HOME, 'db/' 'xapian-msg-index/'))
    
    enquire = xapian.Enquire(database)

    # First we'll restrict the search space by geographical data:

    lng_keywords = []

    if coords['x1'] != 0 and coords['x2'] != 0:   
        for keyword in get_latlng_keywords(coords['x1'],coords['x2']):
            lng_keywords.append("_glngrange_"+keyword)
        
        lng_query = xapian.Query(xapian.Query.OP_VALUE_RANGE,
                         settings.XAPIAN_LONGITUDE_VALUE,
                         xapian.sortable_serialise(coords['x1']),
                         xapian.sortable_serialise(coords['x2']))

    else:
        lng_query = None

    lat_keywords = []
    
    if coords['y1']!= 0 and coords['y2'] != 0:   
        for keyword in get_latlng_keywords(coords['y1'],coords['y2']):
            lat_keywords.append("_glatrange_"+keyword)

        lat_query = xapian.Query(xapian.Query.OP_VALUE_RANGE,
                        settings.XAPIAN_LATITUDE_VALUE,
                         xapian.sortable_serialise(coords['y1']),
                         xapian.sortable_serialise(coords['y2']))
    else:
        lat_query = None

        
    if lat_query and lng_query:
        lat_wordquery = xapian.Query(xapian.Query.OP_OR, lat_keywords)
        lng_wordquery = xapian.Query(xapian.Query.OP_OR, lng_keywords)
        place_wordquery = xapian.Query(xapian.Query.OP_AND, lat_wordquery, lng_wordquery)
        place_query = xapian.Query(xapian.Query.OP_AND, lat_query, lng_query)
        type_query = xapian.Query(xapian.Query.OP_AND, ["_place"])

        place_query = xapian.Query(xapian.Query.OP_AND, type_query, place_query)
        query = xapian.Query(xapian.Query.OP_AND, place_wordquery, place_query)

        enquire.set_query(query)
        matches = enquire.get_mset(offset, search_limit+offset)
        total_matches=matches.get_matches_estimated()

    screen_id_counter = 0    

    # Filter places with keywords and date:
         
    word_issues = None
    terms = None

    if search_string or from_date or to_date or tags:
        word_issues = {}
        
        issue_query = xapian.Query(xapian.Query.OP_AND, ["_issue"])
            
        if search_string:
            stemmer = xapian.Stem("finnish")
            tmp_terms = re.split (r'[\n-/:-?]', to_lower_case(search_string)) 
            terms = []
            for term in tmp_terms:
                if len(term) > 0 and not is_stopword(term):
                    stemmed = stemmer(term)
        #            if stemmed not in variables.stoplist:
                    terms.append(stemmer(to_lower_case(term)))
            
            keyword_query = xapian.Query(xapian.Query.OP_OR, terms)
    
            issue_query = xapian.Query(xapian.Query.OP_AND, issue_query, keyword_query)
    
        if from_date or to_date:
            if from_date == "None":
                from_date = str("19790626095523.000");
            else:
                from_array = from_date.split('/')
                from_date = str(from_array[2]+from_array[1]+from_array[0]+"000000.000");

            if to_date == "None" :
                to_date = str( datetime.now().strftime('%Y%m%d%H%M%S.000') );
            else:
                to_array = to_date.split('/')
                to_date = str(to_array[2]+to_array[1]+to_array[0]+"235959.999");
#                to_date_date = datetime(to_date)
#                to_date= to_date_date.strftime('%Y%m%d%H%M%S.000')

            modified_query = xapian.Query(xapian.Query.OP_VALUE_RANGE, settings.XAPIAN_MODIFIED_FIELD,
                                            xapian.sortable_serialise(float(from_date)),
                                            xapian.sortable_serialise(float(to_date)) )
            created_query = xapian.Query(xapian.Query.OP_VALUE_RANGE, settings.XAPIAN_CREATED_FIELD,
                                            xapian.sortable_serialise(float(from_date)),
                                            xapian.sortable_serialise(float(to_date)) )
            date_query = xapian.Query(xapian.Query.OP_OR, created_query, modified_query)

            issue_query =  xapian.Query(xapian.Query.OP_AND, issue_query, date_query)

        if tags:
            tag_query = xapian.Query(xapian.Query.OP_AND, tags)
            issue_query =  xapian.Query(xapian.Query.OP_AND, issue_query, tag_query)

        enquire.set_query(issue_query)
        word_matches = enquire.get_mset(offset, view_limit)
        total_matches=word_matches.get_matches_estimated()

        if total_matches == 0:
            word_issues = { "-1" : 1}

        else:
            for m in word_matches:
                word_issues[str(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_ID_FIELD))]=1
        

    if lat_query and lng_query:
        places = {}
        if word_issues:
            for m in matches:
                issue = m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_PARENT_ISSUE_FIELD)
                if  word_issues.has_key(issue):
                    y = float(xapian.sortable_unserialise(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_LATITUDE_VALUE)))
                    x = float(xapian.sortable_unserialise(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_LONGITUDE_VALUE)))
        #            if y >= coords['y1'] and y <= coords['y2'] and x >= coords['x1'] and x <= coords['x2']:
                    places[ (m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_PARENT_ISSUE_FIELD))
                            +":"+(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_PARENT_MESSAGE_FIELD))
                            +":"+(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_ID_FIELD))
                           +":"+str(m[xapian.MSET_DOCUMENT].get_data())
                                                                                   ] = [y, x]

        else:        
            for m in matches: 
                y = float(xapian.sortable_unserialise(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_LATITUDE_VALUE)))
                x = float(xapian.sortable_unserialise(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_LONGITUDE_VALUE)))
    #            if y >= coords['y1'] and y <= coords['y2'] and x >= coords['x1'] and x <= coords['x2']:
                places[ (m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_PARENT_ISSUE_FIELD))
                            +":"+(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_PARENT_MESSAGE_FIELD))
                            +":"+(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_ID_FIELD))
                            +":"+str(m[xapian.MSET_DOCUMENT].get_data())
                                                                               ] = [y, x]
        results = ""
        
        # bad kludge to calculate amount of issues and messages in a cluster!
        pmessages = {}
        pissues = {}    
        
        issue_data = []
        issue_ids = {}
    
        shown_issues = {}
            

    if lat_query and lng_query:
        
        if zoomlevel < 16 and len(places)> 1 and cluster > 0:
            total_matches=0

            clusters = map_utils.cluster_map_markers(places, zoomlevel, cluster_threshold_pixels=cluster*cluster_thr_for_zoomlevel[zoomlevel]/50)
    
            issue_ids = []
            message_ids = []
            
            clusters.reverse()
            
            for cluster in clusters: # Reverse the array so clusters are processed and sent first, followed by the single cases.
    #            print cluster
                if len(cluster[0]) == 1:
                    m = cluster[0][0]
                    if 1 == 1:
                        id = m.split(":")[0]
 #                       print "it's an issue! "  + str(id)                       
                        if shown_issues.has_key(id):
                            continue
                        shown_issues[id] = 1
                        total_matches += 1
    #                    print "Issue id: " + str(issue_id)

                        if 1 == 1:
                                enquire.set_query(xapian.Query(xapian.Query.OP_AND, ["_issue_"+m.split(":")[0]]))
                                match = enquire.get_mset(0, 1)
                                if len(match) > 0:
                                    issue_dict=json.loads(match[0][xapian.MSET_DOCUMENT].get_data())
                                    print m.split(":")[0]
                                    print match[0][xapian.MSET_DOCUMENT].get_data()
                                    print len(issue_dict)
                                    if details == "no":
                                        if issue_dict["options"].has_key("comments"):
                                            del issue_dict["options"]['comments']
                                    issue_dict.update({'screen_id' :screen_id_counter})
                                    screen_id_counter += 1
                                    issue_data.append(issue_dict)
                                else:
                                    print "Api.xapian_search a: looking for _issue_" + m.split(":")[0] + " but could not find it!"

                else:
                    issuecount = 0
                    messagecount = 0
    
                    for iss in cluster[0]:
                        if pissues.has_key(str(iss)):
                            issuecount += 1
                            issue_ids.append(iss)
                        elif pmessages.has_key(str(iss)):
                            messagecount += 1
                            message_ids.append(iss)
    
                    
                    
                    issue_places = [ places[(place_id)] for place_id in cluster[0] ]

                    cluster_places = [ place_id.split(":")[2] for place_id in cluster[0] ]
                    cluster_issues = [ place_id.split(":")[0] for place_id in cluster[0] ]
                    cluster_addresses = [ place_id.split(":")[3] for place_id in cluster[0] ]


                    placelinks ={}
                    for i in range(1,len(cluster_places)):
                        if not cluster_issues[i] in placelinks:
                            placelinks[cluster_issues[i]]=( {"place": cluster_addresses[i], "link": "/r/"+cluster_issues[i]+"/"} )


                    title = str(len(placelinks)) + _(" messages in this area") 

                    sw = { 'lat': str(min([place[0] for place in issue_places])), 'lng': str(min([place[1] for place in issue_places]))}
                    ne = { 'lat': str(max([place[0] for place in issue_places])), 'lng': str(max([place[1] for place in issue_places]))}
                        
                    issue_data.append({ 'title': title,
                                        'options': {
                                            'author' : "TODO: not here yet!",
                                            'date' : "TODO: not here yet!",
                                            'points' : [ {'lng':cluster[1][0], 'lat':cluster[1][1]} ],        
                                            'score': 'NONE',
                                            'id': 'NONE',
                                            'status': 'NONE',
                                            'link': 'NONE', 
                                            'icon': {'name':'/images/merkki_klusteri_'+ str(min([max([len(placelinks),2]), 4])) +'.png',
                                                     'activeiconname': '/images/merkki_klusteri_'+ str(min([max([len(placelinks),2]), 4])) +'_fully_red.png',
                                                     'partlyactiveiconname': '/images/merkki_klusteri_'+ str(min([max([len(placelinks),2]), 4])) +'_partly_red.png',
                                                     'w': 41,
                                                     'h': 46,
                                                     'ax': 10,
                                                     'ay': 44,
                                                     },
                                            'places':cluster_places,
                                            'issues' : len(placelinks),
#                                            'messages' : message_ids,
                                            'type':'cluster',
                                            'sw': sw,
                                            'ne': ne,
                                            'placelinks' : [{"place": value["place"],"link": value["link"] } for value in placelinks.values()],
                                            },
                                        'point':  {'lon': cluster[1][0], 'lat':cluster[1][1]}, 
                                        'screen_id' : screen_id_counter})

                    screen_id_counter+= 1
        
        else:
            total_matches=len(places)

            for m in places.keys():
                id = m.split(":")[0]

                enquire.set_query(xapian.Query(xapian.Query.OP_AND, ["_issue_"+m.split(":")[0]]))
                match = enquire.get_mset(0, 1)
                if len(match) > 0:
                    issue_dict=json.loads(match[0][xapian.MSET_DOCUMENT].get_data())
                    if details == "no":
                            if issue_dict["options"].has_key("comments"):
                                del issue_dict["options"]['comments']
                    issue_dict.update({'screen_id' :screen_id_counter})

                    screen_id_counter += 1
                    issue_data.append(issue_dict)
                else:

                    print "Api.xapian_search b: looking for _issue_" + m.split(":")[0] + " but could not find it!"
    else:
        issue_data=[]
        for m in word_matches:
                itemtype=str(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_DATATYPE_FIELD))
                itemid=str(m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_ID_FIELD))                
                issue_dict = json.loads(m[xapian.MSET_DOCUMENT].get_data())
                if details == "no":
                        if issue_dict["options"].has_key("comments"):
                            del issue_dict["options"]['comments']
                issue_dict.update({'screen_id' :screen_id_counter})
                screen_id_counter += 1
                issue_data.append(issue_dict)


    # this rather complicated procedure goes through the text fields
    # and finds the relevant words there:

    if terms:    
        for issue in issue_data: 

                       
            newtitle = ""
            for word in re.split(r'([\n-/:-?])', issue["title"]):
                stemmed = stemmer(to_lower_case(word))
                match1 = 0
                for term in terms:
                    if term == stemmed:
                        newtitle += ' <span class="keywordhighlight">' + word + '</span>'
                        match1 = 1
                        break 
                if match1 == 0:
                    newtitle += word
            
            issue["title"] = newtitle     

            relevant_string= ""
            
            if issue["options"].has_key("comments"):
                for msg in issue["options"]["comments"]:
                    content = ""
                    selected_words = {}
                    if msg.has_key("text"):
                        word_array = re.split(r'([ \n-/:-?])', msg["text"])

                        index = -1
                        for word in word_array:
                            index += 1
                            if len(word) > 1:
                                stemmed = stemmer(to_lower_case(word))
                                for term in terms:
                                    if term == stemmed:
                                        selected_words[index] = 1
                                        word_array[index] = ' <span class="keywordhighlight">' + word + '</span>'
                                        for i in range (1, 12):
                                            if index + i < len(word_array):
                                                selected_words[index + i] = 1
                                        for i in range (1, 12):
                                            if index - i >= 0:
                                                selected_words[index - i] = 1
                                        break

                        oldindex = 0
    #                    if len(selected_words) == 0:
    #                        for i in range (0, 25):
    #                            if i < len(word_array):
    #                                selected_words[i] = 1

    #                    if not selected_words.has_key(0):
                            #content += " ... "
    #                        continue

                        for index in sorted(selected_words.keys()):
                            if index > oldindex + 1:
                                content += " ... "
                            content += word_array[index]
                            oldindex = index
                        if oldindex < len(word_array):
                            content += " ... "


                        if len(content) > 7:
                            relevant_string += content


        
                if len(relevant_string) > 0:
                    issue["search_hit_string"] = relevant_string


    metadata = {'seqnum':seqnum,
                'total_matches': total_matches,
                'first_shown_match' : str(min(offset+1, len(issue_data))),
                'last_shown_match': str(offset+len(issue_data)),
                'shown_matches': str(offset)+"-"+str(offset+len(issue_data) )}
        
    return HttpResponse(dumps([metadata,issue_data]))



        
        

def to_lower_case(word):
    word = re.sub('Ä', 'ä', word)
    word = re.sub('Ö', 'ö', word)
    word = re.sub('Å', 'å', word)
    word = re.sub('Ü', 'ü', word)
    word = re.sub('Á', 'á', word)
    word = re.sub('À', 'à', word)
    word = re.sub('É', 'é', word)
    word = re.sub('È', 'è', word)
    word = re.sub('[/,.-;:!?\']', ' ', word)
    return word.lower()



def is_stopword(word):
    return word in settings.XAP_STOPWORDS


@json_resp
def search_data_2(request):
    if not xapian_avail:
        return HttpResponse('{}')

    search_string = request.GET.get('keywords', '')
    search_limit = int(request.GET.get('slimit', str(settings.MAX_MATCHES_SEARCH)))
    view_limit = int(request.GET.get('vlimit', str(settings.MAX_MATCHES_SHOW)))
    search_offset = int(request.GET.get('offset', '0'))
    search_max_result_length = int(request.GET.get('maxchars', '0'))

    seqnum = int(request.GET.get('seqnum', 0))
    
    returnarray = []
    
    database = xapian.Database(settings.XAPIAN_DATABASE_HOME)

    enquire = xapian.Enquire(database)

    stemmer = xapian.Stem("finnish")

    tmp_terms = re.split (r'[\n-/:-?]', to_lower_case(search_string)) 

    terms = []
    for term in tmp_terms:
        if len(term) > 0 and not is_stopword(term):
            stemmed = stemmer(term)
#            if stemmed not in variables.stoplist:
            terms.append(stemmer(to_lower_case(term)))

    query = xapian.Query(xapian.Query.OP_OR, terms)
    enquire.set_query(query)
    matches = enquire.get_mset(0, search_limit)
#    print "%i results found" % matches.get_matches_estimated() 
#    for m in matches:
#        print m[xapian.MSET_DOCUMENT].get_data() + " --- relevance: " + str(m[xapian.MSET_PERCENT])

    tmp_term_string = ""
    for term in terms:
        tmp_term_string += term + " "

    match_array = [tuple(m[xapian.MSET_DOCUMENT].get_data().split(':')) for m in matches]

    db = roundup_utils.db()
    issues = db.issue.list()

#    print "This should go to terminal, right?"

    result_issues = []
    result_messages = {}

    for match in match_array:
        
#        print str(match)
        
        if match[0] == 'issue':
            if not match[1] in result_issues:
                result_issues.append((match[1]))
        elif match[0] == 'msg':
            if not db.issue.find(messages={str(match[1]):1 })[0] in result_issues:
                result_issues.append(db.issue.find(messages={str(match[1]):1 })[0])
            result_messages[match[1]] = match[1]

    counter = 0;
    for match in result_issues: 
        counter += 1       
        if counter > view_limit:
            break

        issue = db.issue.getnode(match)
                   
        title = ""
        for word in re.split(r'([\n-/:-?])', issue.title):
            stemmed = stemmer(to_lower_case(word))
            match1 = 0
            for term in terms:
                if term == stemmed:
                    title += ' <span class="keywordhighlight">' + word + '</span>'
                    match1 = 1
                    break 
            if match1 == 0:
                title += word
             
        msg_hits = []

        for msg in issue.messages:
            if msg in result_messages:
                msg_hits.append(msg)
            
        content = ""
        
        for match_id in msg_hits: 
            msg = db.msg.getnode(match_id)
            
            selected_words = {}
            word_array = re.split(r'([ \n-/:-?])', msg.content)


            index = -1
            for word in word_array:
                index += 1
                if len(word) > 1:
                    stemmed = stemmer(to_lower_case(word))
                    for term in terms:
                        if term == stemmed:
                            selected_words[index] = 1
                            word_array[index] = ' <span class="keywordhighlight">' + word + '</span>'
                            for i in range (1, 25):
                                if index + i < len(word_array):
                                    selected_words[index + i] = 1
                            for i in range (1, 25):
                                if index - i >= 0:
                                    selected_words[index - i] = 1
                            break 
            
            oldindex = 0
            if len(selected_words) == 0:
                for i in range (0, 25):
                    if i < len(word_array):
                        selected_words[i] = 1
            
            if not selected_words.has_key(0):
                content += " ... "
            
            for index in sorted(selected_words.keys()):
                if index > oldindex + 1:
                    content += " ... "
                content += word_array[index]
                oldindex = index
            if oldindex < len(word_array):
                content += " ... "

            #TODO Fix this link to point to actual thing!
        content += " <a href=\"" + reverse('report_view', args=[match]) + "\">> " + _(u'Read more and comment').encode('utf-8') + "</a>"
 
        returnarray.append({ 
                            'seqnum':  seqnum,
                            'title': title,
                            'content':  content,
                            'date': 'yesterday',
                            'author': 'Milla Magia',
                            })

    if len(returnarray) < 1:
        returnarray.append({'seqnum':  seqnum,
                            'title': "",
                            'content':  _(u'Kun alat kirjoittaa, näytämme tässä samankaltaisia viestejä'),
                            })
        
 
    return HttpResponse(dumps(returnarray))
 
 
@json_resp
def popular_issue_data(request):

    view_limit = int(request.GET.get('vlimit', str(settings.MAX_MATCHES_SHOW)))
    search_offset = int(request.GET.get('offset', '0'))
    search_max_result_length = int(request.GET.get('maxchars', '0'))

    popular_messages = get_popular_messages(count=view_limit, offset=search_offset, filters=None)

    return HttpResponse(dumps(popular_messages))

@json_resp
def latest_issue_data(request):
    
    view_limit = int(request.GET.get('vlimit', str(settings.MAX_MATCHES_SHOW)))
    search_offset = int(request.GET.get('offset', '0'))
    search_max_result_length = int(request.GET.get('maxchars', '0'))
    
    latest_messages = get_latest_messages(count=view_limit, offset=search_offset, filters=None)

    return HttpResponse(dumps(latest_messages))
    

@json_resp
def official_issue_data(request):

    view_limit = int(request.GET.get('vlimit', str(settings.MAX_MATCHES_SHOW)))
    search_offset = int(request.GET.get('offset', '0'))
    search_max_result_length = int(request.GET.get('maxchars', '0'))

    official_messages = get_officer_messages(count=view_limit, offset=search_offset, organisations=[4,6],filters=None)

    return HttpResponse(dumps(official_messages))


 
@never_cache
@json_resp
def comment_data(request):
    issue_id = request.GET.get('issue_id', '')

#    print ("getting comment data! for issue " + issue_id)

    returnarray = get_votes(issue_id, roundup_utils.get_user_id(request))

    return HttpResponse(dumps(returnarray))

@never_cache
@json_resp
def single_issue_data(request):
    issue_id = str(request.GET.get('id', '1').encode('ASCII'))

    returnarray = issue_dict=issue_to_dict(None,issue_id=issue_id)

    return HttpResponse(dumps(returnarray))
    

@never_cache
@json_resp
def vote_comment(request):
#    print "Starting vote:"
    
    message_id = str(request.GET.get('message_id', '').encode('ascii'))
    issue_id = str(request.GET.get('issue_id', '').encode('ascii'))
    score = str(request.GET.get('score', '').encode('ascii'))

#    print "voting for " + score + " message " + message_id 

    db = roundup_utils.db()
    
    user_id = roundup_utils.get_user_id(request)

    #cast vote here
    voteset = False

    if message_id == "-1":
#        print "voting for issue " + issue_id
        if request.session.has_key('_issue_votecast_' + issue_id):
#            print "session has vote key for " + issue_id
            if db.vote.hasnode(request.session['_issue_votecast_' + issue_id]):
                    db.vote.set(request.session['_issue_votecast_' + issue_id], value=score)
                    voteset = True
        
        elif not roundup_utils.is_anon_user(request):
#            print "User is nr " + user_id
      
            vote_ids = db.vote.find(author={user_id:1})
            
            if vote_ids:
                for vote_id in vote_ids:
                    vote = db.vote.getnode(vote_id)
                    if  vote.issue == issue_id:
                        db.vote.set(vote_id, value=score)
                        voteset = True
                        request.session['_issue_votecast_' + issue_id] = vote_id
        
        if voteset == False:
            print "new vote generated..."
            this_vote_id = db.vote.create(
                value=score,
                author=user_id,
                issue=issue_id,
            )
            print "New vote generated: " + this_vote_id
    
            request.session['_issue_votecast_' + issue_id] = this_vote_id
  
            issue = db.issue.getnode(issue_id)
            issue.votes += [ this_vote_id ]

    else:
        print "voting for comment " + message_id
        
        if request.session.has_key('_comment_votecast_' + message_id):
            print "session has vote key for " + message_id
            if db.vote.hasnode(request.session['_comment_votecast_' + message_id]):
                print "Adding vote to message pt. 1!"

                db.vote.set(request.session['_comment_votecast_' + message_id], value=score)
                voteset = True
    
        elif not roundup_utils.is_anon_user(request):
#            print "User is nr " + user_id
      
            vote_ids = db.vote.find(author={user_id:1})
            
            if vote_ids:
                for vote_id in vote_ids:
                    vote = db.vote.getnode(vote_id)
                    if  vote.message == message_id:
                        print "Adding vote to message pt. 2!"

                        db.vote.set(vote_id, value=score)
                        voteset = True
                        request.session['_comment_votecast_' + message_id] = vote_id
    
        
        if voteset == False:
 #           print "new vote generated..."
            this_vote_id = db.vote.create(
                value=score,
                author=user_id,
                message=message_id,
            )
 #           print "New vote generated: " + this_vote_id
    
            request.session['_comment_votecast_' + message_id] = this_vote_id

 #           print "Adding vote to message pt. 3!"

            message = db.msg.getnode(message_id)
            message.votes += [ this_vote_id ]
    
 #   print "Committing to db!"


    db.commit()
    db.close()
    
#    print "db closed, now returning comment data"

    returnarray = get_votes(issue_id, roundup_utils.get_user_id(request))

    return HttpResponse(dumps(returnarray))
        



def get_votes(issue_id, user_id):

    db = roundup_utils.db()

    if db.issue.hasnode(issue_id):
        issue = db.issue.getnode(issue_id)
        vote_ids = issue.votes 
    else:
 #       print "issue " + str(issue_id) + " does not seem to exist?"
        vote_ids = []

 #   print "Votes for issue " + str(issue_id) + ": " + str(vote_ids)
    votesFor = 0
    votesAgainst = 0
    
    votecast = ""
    
    for v in vote_ids:
        vote = db.vote.getnode(v)
        if vote.value == "1":
            votesFor += 1
        elif vote.value == "-1":
            votesAgainst += 1
        if vote.author == user_id:
            votecastid = vote.id
            votecast = vote.value
        
    if votecast == "":
#        if request.session.has_key('_votecast_issue_'+issue_id):
#            votecast = request.session.has_key('_votecast_issue_'+issue_id)
#        else:
            votecast = 0

    if db.issue.hasnode(issue_id):
        issue = db.issue.getnode(issue_id)
        score = issue.score    
    else:
        score = '0'
    
    returnarray = [{'issue_id': issue_id,
                        'issue_votesfor' : str(votesFor),
                        'issue_votesagainst': str(votesAgainst),
                        'votecast' : votecast,
                        'issue_score': str(score),
                        }]
    
    
    for msg_id in db.issue.getnode(issue_id).messages:
        
        vote_ids = db.vote.find(message={msg_id:1 })
        votesFor = 0
        votesAgainst = 0
        
        votecast = ""
            
        for v in vote_ids:
            vote = db.vote.getnode(v)
            if vote.value == "1":
                votesFor += 1
            elif vote.value == "-1":
                votesAgainst += 1
            if vote.author == user_id:
                votecastid = vote.id
                votecast = vote.value
 
         
#        if votecast == "":
#            if request.session.has_key('_votecast_comment_'+msg_id):
#                votecast = request.session.has_key('_votecast_comment_'+msg_id)
#            else:
#                votecast = 0
        
        returnarray.append({'comment_id': db.msg.getnode(msg_id).id,
                            'issue_id': issue_id,
                            'votesfor' : str(votesFor),
                            'votesagainst': str(votesAgainst),
                            'votecast' : votecast,
                            'issue_score': 'F',
                            })

    return returnarray

@never_cache
@json_resp
def issue_file_upload(request):
    print "image being uploaded !"
    return_array = []
    return_array.append({'filename': "aatamo" })
    return_array.append({'filename': "barttol" })
    return_array.append({'filename': "sejamati" })
    return HttpResponse(dumps(return_array))



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@never_cache
@json_resp
def add_issue(request):
    return HttpResponse(dumps(adding_through_api.add_message_through_api(request)))