#coding=UTF-8

from django import template
from django.utils.translation import ungettext, ugettext as _
import datetime
from django.conf import settings
from hila import map_utils

from datetime import datetime
from django.core.urlresolvers import reverse
import random, os, re, datetime
from django.conf import settings

from django.utils.translation import ugettext as _

import simplejson
#from gwibber.actions import tag

try:
    import xapian
    xapian_avail = True
except ImportError:
    logging.warning('Failed to import xapian, search disabled')
    xapian_avail = False




#
# Originally from http://www.djangosnippets.org/snippets/1409/
#
#@register.filter
def smart_date_diff(d):

    #
    # Kludged time difference here - fix before daylight saving starts! rk 12/06/2009
    #
    d = d + datetime.timedelta(hours=3)

    
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)
    delta = now - d
    delta_midnight = today - d
    days = delta.days
    hours = round(delta.seconds / 3600., 0)
    minutes = round(delta.seconds / 60., 0)
    chunks = (
        (365.0, lambda n: ungettext('year', 'years', n)),
        (30.0, lambda n: ungettext('month', 'months', n)),
        (7.0, lambda n : ungettext('week', 'weeks', n)),
        (1.0, lambda n : ungettext('day', 'days', n)),
    )
    
    if days == 0:
        if hours == 0:
            if minutes > 0:
                return ungettext('1 minute ago', \
                    '%(minutes)d minutes ago', minutes) % \
                    {'minutes': minutes}
            else:
                return _("less than 1 minute ago")
        else:
            return ungettext('1 hour ago', '%(hours)d hours ago', hours) \
            % {'hours':hours}

    if delta_midnight.days == 0:
        return _("yesterday at %s") % d.strftime("%H:%M")

#    if days > 0:
#        return _(d.strftime("%d.%m.%Y"))
    
    count = 0
    for i, (chunk, name) in enumerate(chunks):
        if days >= chunk:
            count = round((delta_midnight.days + 1)/chunk, 0)
            break

    return _('%(number)d %(type)s ago') % \
        {'number': count, 'type': name(count)}


def add_smart_dates(issuedict):
    if issuedict["options"].has_key("date"):
        d=issuedict["options"]["date"]
        issuedict["options"].update({"smartdate": smart_date_diff(datetime.datetime(
            int(d[0:4]),int(d[5:7]),int(d[8:10]),int(d[11:13]),int(d[14:16]),int(d[17:19])
        ))})
    if issuedict["options"].has_key("latest_comment_date"):
        d=issuedict["options"]["latest_comment_date"]
        issuedict["options"].update({"latest_comment_smartdate": smart_date_diff(datetime.datetime(
            int(d[0:4]),int(d[5:7]),int(d[8:10]),int(d[11:13]),int(d[14:16]),int(d[17:19])
        ))})
    if issuedict["options"].has_key("comments"):
        for comment in issuedict["options"]["comments"]:
            d=comment["date"]
            comment.update({"smartdate": smart_date_diff(datetime.datetime(
                int(d[0:4]),int(d[5:7]),int(d[8:10]),int(d[11:13]),int(d[14:16]),int(d[17:19])
            ))})




def get_popular_messages(count=10,offset=0, filters=None):

    popular_messages = []
    
    database = xapian.Database(settings.TRACKER_HOME + '/db/text-index')
    enquire = xapian.Enquire(database)

    query = xapian.Query(xapian.Query.OP_OR, [''])
    enquire.set_query(query)
    enquire.set_sort_by_value(settings.XAPIAN_ISSUE_SCORE_VALUE)
    matches = enquire.get_mset(0, settings.MAX_SEARCH_LIMIT)

    match_array = [tuple(m[xapian.MSET_DOCUMENT].get_data().split(':')) for m in matches]

    from hila import roundup_utils

    db = roundup_utils.db()
    
    shown_messages = {}

    for match in match_array:
 #       print str(match)
        if match[0] == 'issue':
            if db.issue.hasnode(match[1]) and not shown_messages.has_key(match[1]):
                shown_messages[match[1]] = 1
                if offset > 0:
                    offset =- 1
                else:
                    popular_messages.append(issue_to_dict(issue=db.issue.getnode(match[1]), db=db))

    return popular_messages


def get_latest_messages(count=10,offset=0, filters=None, tag=None):

#    print "Getting latest messages:"


    import xapian

    from hila import roundup_utils

    db = roundup_utils.db()

    database = xapian.Database( os.path.join(settings.TRACKER_HOME, 'db/' 'xapian-msg-index/'))
    enquire = xapian.Enquire(database)

    query = xapian.Query(xapian.Query.OP_AND, ["_issue"])

    if tag:
        tagquery = xapian.Query(xapian.Query.OP_AND, ["_key_"+tag])
        query = xapian.Query(xapian.Query.OP_AND, query, tagquery)

    enquire.set_query(query)
    enquire.set_sort_by_value(settings.XAPIAN_MODIFIED_FIELD, reverse=True)
    matches = enquire.get_mset(0,count)


    rval = [ simplejson.loads(m[xapian.MSET_DOCUMENT].get_data()) for m in matches ]


    for issue in rval:
        add_smart_dates(issue)

    return rval


def get_latest_issues(count=10,offset=0, filters=None, tag=None):

#    print "Getting latest messages:"


    import xapian

    from hila import roundup_utils

    db = roundup_utils.db()

    database = xapian.Database( os.path.join(settings.TRACKER_HOME, 'db/' 'xapian-msg-index/'))
    enquire = xapian.Enquire(database)

    query = xapian.Query(xapian.Query.OP_AND, ["_issue"])

    if tag:
        tagquery = xapian.Query(xapian.Query.OP_AND, ["_key_"+tag])
        query = xapian.Query(xapian.Query.OP_AND, query, tagquery)

    enquire.set_query(query)
    enquire.set_sort_by_value(settings.XAPIAN_CREATED_FIELD, reverse=True)
    matches = enquire.get_mset(0,count)


    rval = [ simplejson.loads(m[xapian.MSET_DOCUMENT].get_data()) for m in matches ]


    for issue in rval:
        add_smart_dates(issue)
        if issue['options'].has_key('comments'):
            del issue['options']['comments']

    return rval



"""
def get_latest_issues(count=10,offset=0, filters=None):

 #   print "Getting latest issues:"
    
    from hila import roundup_utils

    db = roundup_utils.db()

    issues = db.issue.list()
    latest_message_count=min(len(issues), count )
    
#    print "latest message count: " + str(latest_message_count)
    
#    print "offset: " + str(offset)
    if offset == 0:
        latest_issues = issues[-latest_message_count:]
    else:
        latest_issues = issues[-latest_message_count-offset:-offset]
    latest_issues.reverse()

#    print "returning "+ str(len(latest_issues))

    return [ issue_to_dict(issue=db.issue.getnode(issue_id)) for issue_id in latest_issues ]
"""


def get_latest_comments(count=10,offset=0, filters=None, tag=None):

#    print "Getting latest messages:"

    import xapian

    from hila import roundup_utils

    database = xapian.Database( os.path.join(settings.TRACKER_HOME, 'db/' 'xapian-msg-index/'))
    enquire = xapian.Enquire(database)

    query = xapian.Query(xapian.Query.OP_AND, ["_msg"])

    if tag:
        tagquery = xapian.Query(xapian.Query.OP_AND, ["_key_"+tag])
        query = xapian.Query(xapian.Query.OP_AND, query, tagquery)

    enquire.set_query(query)
    enquire.set_sort_by_value(settings.XAPIAN_CREATED_FIELD, reverse=True)
    matches = enquire.get_mset(0,count)

    return [ simplejson.loads(m[xapian.MSET_DOCUMENT].get_data()) for m in matches ]



def get_officer_messages(count=10,offset=0, filters=None, organisations=[], tag=None):

    import xapian

    database = xapian.Database( os.path.join(settings.TRACKER_HOME, 'db/' 'xapian-msg-index/'))
    enquire = xapian.Enquire(database)

    typequery = xapian.Query(xapian.Query.OP_OR, ["_msg", "_issue"])

    officialquery =  xapian.Query(xapian.Query.OP_OR, ["_group_"+str(id) for id in organisations])


    query = xapian.Query(xapian.Query.OP_AND, typequery, officialquery)

    if tag:
        tagquery = xapian.Query(xapian.Query.OP_AND, ["_key_"+tag])
        query = xapian.Query(xapian.Query.OP_AND, query, tagquery)


    enquire.set_query(query)
    enquire.set_sort_by_value(settings.XAPIAN_CREATED_FIELD, reverse=True)
    matches = enquire.get_mset(offset,count)


    rval =[]
    for m in matches:
        if m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_DATATYPE_FIELD) == "issue":
            rval.append(simplejson.loads(m[xapian.MSET_DOCUMENT].get_data()))
        else:
            query = xapian.Query(xapian.Query.OP_AND, ["_issue_"+m[xapian.MSET_DOCUMENT].get_value(settings.XAPIAN_PARENT_ISSUE_FIELD)])
            enquire.set_query(query)
            rval.append(simplejson.loads(enquire.get_mset(0,1)[0][xapian.MSET_DOCUMENT].get_data()))

    return rval




def issue_to_dict(issue=None, issue_id=None, db=None):
    from hila import roundup_utils
    return roundup_utils.issue_to_dict(issue, issue_id, db=db)

def issue_to_quick_dict(issue=None, issue_id=None, db=None):
    from hila import roundup_utils
    return roundup_utils.issue_to_quick_dict(issue, issue_id, db=db)


def get_image_thumbnail(file_id, w, h):
    
    if file_id is None:
        print "!!!!!!!!!!!!!! returning none from get_image_thumbnail!!!!!!!!!!!!!"
        return None

    from hila import roundup_utils

    db = roundup_utils.db()
    
    this_file = db.file.getnode(file_id)

    thumburl =   '/messageimages/'+str(w)+'x'+str(h)+'/'+ this_file.id + '_' + this_file.name
#    print "Checking if thumbnail exists: " + settings.MEDIA_ROOT + thumburl
    if not os.path.exists( settings.MEDIA_ROOT + thumburl ):
#        print "create thumbnails into "+settings.MEDIA_ROOT + thumburl 
        # We use PIL's Image object
        # Docs: http://www.pythonware.com/library/pil/handbook/image.htm
        from PIL import Image
    
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (w, h)
    
        # Save fake thumbnail as empty so we can get the filename from the 
        # original filename, from Django's convenience method 
        # get_FIELD_filename()
   
        # Open original photo which we want to thumbnail using PIL's Image
        # object
        image = Image.open( settings.TRACKER_HOME + '/db/files/file/0/file'+this_file.id)
    
        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
    
        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        
        print "Saving thumbnail to " + settings.MEDIA_ROOT + thumburl 
        # Save the thumbnail
        image.save( settings.MEDIA_ROOT + thumburl)

    return settings.MEDIA_URL + thumburl


from hila.public.report.models import Theme

def get_tag_decorations(tag=None):

    decorations = {"allow_creation": 1,
                   "allow_commenting": True}

    if tag is not None:
        try:
            tag = Theme.objects.filter(name__exact=tag)[0]
        except IndexError:
            return {'error':'invalid API key'}

        decorations.update({"custom_selected_tagfilter": tag.name,
                            "custom_description": tag.description,
                            "custom_css":  tag.custom_css,
                            "custom_logo_dir" : tag.custom_logo,
                            "custom_add_new_button_dir": tag.custom_create_logo,
                            "custom_javascript": tag.custom_javascript,
                            "custom_front_url":  reverse('public_themed_front', args=[tag]),
                            "custom_ingress": tag.custom_ingress_short,
                            "allow_creation": tag.allow_issue_creation(),
                            "allow_commenting": tag.allow_commenting(),
                            })

    return decorations
"""
        if tag == "talvikysely":

            decorations.update ({"custom_selected_tagfilter": "talvikysely",
                                 "custom_css": "<style type='text/css'> body {background-image: url('"+ settings.MEDIA_URL+"images/talvikysely/fillarikanava_layout_1_9_winter.jpg');}\
            .ingress_column { text-align: left; float: left; width: 400px; padding: 0px 20px 0px 20px }</style>",
                                 "custom_logo_dir": settings.MEDIA_URL+"images/talvikysely/",
                                 "custom_add_new_button_dir": settings.MEDIA_URL+"images/talvikysely/",
                                 "custom_javascript": '<script type="text/javascript" src="'+ settings.MEDIA_URL+'js/talvikysely.js"></script>',
    #                             "custom_create_url": reverse("talvikysely_report_create", args=['talvikysely']),
                                 "custom_front_url" :reverse("public_talvikysely", args=[]),
                                 "custom_ingress" :  u"\
                                 <h3>Talvikysely on päättynyt, kiitokset kaikille vastaajille // Winter survey is over, thanks to all the participants  </h3>\
    <p>"+_( u" Kyselyllä (13.4. - 11.5.2010) kartoitetaan keskeisimpiä \n\
    työmatkapyöräilyn reittejä ja niihin riittyviä huomioita. Lisätietoja                      \n\
    <a href=\"http://www.hel.fi/wps/portal/Rakennusvirasto/Kadut?WCM_GLOBAL_CONTEXT=/hkr/fi/Kadut\">rakennusviraston sivulla</a>.    </p>     \n\
    ")+"                             </p> \
         <div id=\"first_time_info_open\" class=\"hidden\">  \
                 <a href=\"#\" onClick=\"openFirstTimeInfo()\">"+_(u"More info")+"<img src=\""+settings.MEDIA_URL +"/images/icons/silk_icons/arrow_down.png\" alt=\"more info\"/></a>\
        </div>\
        <div id=\"first_time_info\" style=\"border:1px solid;\" >   \
           <div class=\"ingress_column\"> \
    <p>"+_(u"Kartalla näkyy keskustelun herättämiseksi tarkoitettu alustava         \
    ehdotus. Kerro ja merkitse kartalle omat kommenttisi tai kommentoi     \
    muiden käyttäjien jättämiä huomioita.")+"                                   \
    <ul>                                                                    \
     <li>"+_(u"Onko ehdotettu reitti hyvä, mikä voisi olla parempi pääyhteys?")+" </li> \
     <li>"+_(u"Mitä yksityiskohtaisia huomioita tai parannuskohteita väylään liittyy?")+"</li>\
     <li>"+_(u"Puuttuuko suunnitelmasta jokin tärkeä yhteys?     ")+"  </li>              \
     <li>"+_(u"Miten talvikunnossapito kyseisellä reitillä voisi parantaa? ")+"</li>      \
    </ul>                                                                 \
    <p>                                                                      \
    "+_(u"Kartoituksen avulla valitaan kokonaispituudeltaan n.100 km osa              \
    pääverkostoa, jolle tehdään kuntokartoitus ja tehostetun                    \
    talvikunnossapidon suunnitelma. Rakennusvirastossa hankkeesta vastaa        \
    Penelope Sala-Sorsimo. Viestinnästä, palautteen keruusta ja                 \
    koostamisesta vastaa Antti Poikola.")+"                                         \
    </p></div>                 \
        <div class=\"ingress_column\">\
             <div id=\"close_button\" style=\"float:right;\">   \
                 <a href=\"#\" onClick=\"closeFirstTimeInfo()\">"+_(u"Close")+"<img src=\""+settings.MEDIA_URL +"/images/icons/silk_icons/arrow_up.png\" alt=\""+_(u"close")+"\"/></a>  \
             </div> \
    <p>"+u"                                                                            \
    "+_(u"Talvikyselyyn jätetyt viestit tallentuvat muiden Fillarikanavaan            \
    jätettyjen viestien yhteyteen ja jo aiemmin samoihin reitteihin             \
    kohdistetut viestit huomioidaan myös Talvikyselyn tulosten                  \
    koostamisessa.")+"                                                              \
    </p><p>                                                                            \
    "+_(u"Esitä asia ensin ytimekkäästi (140 merkkiä, näkyvät kartalla), sen          \
    jälkeen voit kommentoida omaa viestiäsi ilman merkkirajoitusta (näkyy       \
    viestiketjussa).")+"                                                            \
    </p><p>                                                                            \
    "+_(u"Anonyymi palaute on sallittu, mutta Fillarikanavan ylläpito arpoo           \
    11.5. kaikkien rekisteröityjen talvikyselyyn vastanneiden kesken            \
    nastarenkaat (arvo 60-100€), voittajalle ilmoitetaan sähköpostitse.")+"         \
    <a href=\"/accounts/signup/\">"+_(u"Rekisteröidy tästä</a>.")+" </p> \
        </div>        \
     \
    </div>  " } )

    return decorations

    """
