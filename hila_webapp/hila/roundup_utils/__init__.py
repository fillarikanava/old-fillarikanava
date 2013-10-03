from django.conf import settings
from django.http import Http404
from roundup import instance
from roundup import password
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django.utils.encoding import force_unicode, smart_str, smart_unicode
from django.core.exceptions import ObjectDoesNotExist

from roundup.date import Date
from util.misc_utils import smart_date_diff, get_image_thumbnail
from datetime import datetime
import random, os, re, datetime


global db

def tracker(directory=settings.TRACKER_HOME):
    return instance.open(directory)

def db(user='admin'):
    return tracker().open(user)

def node_or_404(klass, id):
    try:
        node = klass.getnode(id)
    except IndexError:
        pass
    if node is None:
        raise Http404, 'Node %s:%d not found' % (klass.__class__.__name__, id)
    return node

def get_tracker_home():
    return settings.TRACKER_HOME

def create_user(username=None, screenname='', title='', address=None, alternate_addresses='', organisation=[], timezone=3, roles=None, passwd=None):
    if address is None or username is None:
        return
    db = tracker().open('admin')

    print "Trying to create user: username >"+str(username)+"< screenname >"+str(screenname)+"<"+\
            " title >"+str(title)+"< address >"+str(address) + "< organisation >"+str(organisation)+"<"+\
             " alt_addresses >" +str(alternate_addresses)+"<"

    if address is None or len(address) < 5:
        if re.match(r'^[0-9]+$',username):
            address=username+"@this.is.facebook.ac"
            print "new address is "+address

#    print str(userdata)
    id = db.user.create(username=username, 
                        screenname=screenname,
                        title=title, 
                        address=address, 
                        password=password.Password(passwd),
                        organisation=organisation,
                        alternate_addresses=alternate_addresses
                        )
    db.commit()
    db.close()
    return id    


def update_user(id=None, username=None, screenname=None, address=None, alternate_addresses=None, organisation=None, timezone=None, roles=None, passwd=None):
    if id is None and username is None:
        return False
    db = tracker().open('admin')
    
    
    if id is None:        
        id = db.user.lookup(username)
        
    if screenname is not None:
        db.user.set(id, screenname=screenname)
    if address is not None:
        db.user.set(id, address=address)
    if alternate_addresses is not None:
        db.user.set(id, alternate_addresses=alternate_addresses)
    if organisation is not None:
        db.user.set(id, organisation=organisation)
    if timezone is not None:
        db.user.set(id, timezone=timezone)
    if roles is not None:
        db.user.set(id, roles=roles)
    if passwd is not None:
        db.user.set(id, password=password.Password(passwd))

    db.commit()
    db.close()
    return True

 
def getnode(node):
    db = tracker().open('admin')
    getnode = db.user.getnode(node)
    db.close()
    return getnode

def test_uniqueness(field=None, value=None):
    db = tracker().open('admin')
    if field and value:
        try:
            db.user.setkey(field)
            user = db.user.lookup(value)
            db.close()
        except KeyError:
            raise User.DoesNotExist
        return user
    else:
        raise KeyError

def create_place(lng='', lat='', address='',city='',postalcode='', country='', issue=None, message=None, issue_id=None, message_id=None, author=None):
    if float(lng)>= -180 and float(lng)<= 180 and float(lat)>= -180 and float(lat)<= 180:
        db = tracker().open('admin')
        node_id = db.place.create(lng=lng,
                lat=lat,
                address=address,
                postalcode=postalcode,
                city=city,
                country=country)
        
        if issue is not None or issue_id is not None:
            if issue is None:
                issue=db.issue.getnode(issue_id)

            if issue.places is not None and len(issue.places) > 0:
                issue.places += [ node_id ]
            else:
                issue.places = [ node_id ]
        
        elif message is not None or message_id is not None:
            if message is None:
                message=db.msg.getnode(message_id)
                
            if message.places is not None and len(message.places) > 0:
                message.places +=  [ node_id ]
            else:
                message.places = [ node_id ]

        db.commit()
        db.close()
        return node_id
    else:
        return None    


def create_file(name='', content='', issue=None, message=None, issue_id=None, message_id=None, author=None):
    db = tracker().open('admin')
    node_id = db.file.create(name=name, content=content)

    if issue is not None or issue_id is not None:
        if issue is None:
            issue=db.issue.getnode(issue_id)

        if issue.files is not None and len(issue.files) > 0:
            issue.files += [ node_id ]
        else:
            issue.files = [ node_id ]
    
    elif message is not None or message_id is not None:
        if message is None:
            message=db.msg.getnode(message_id)
            
        if message.files is not None and len(message.files) > 0:
            message.files +=  [ node_id ]
        else:
            message.files = [ node_id ]
    db.commit()
    db.close()
    return node_id



def create_issue(title=None, status='2', priority='3', score='0', date=None,keywords=None, author=None):
    db = tracker().open('admin')

    if date is None:
        date = Date()

    issue_keywords = []

    if keywords is not None:
        for keyword in keywords:
            if len(keyword) >0 :
                issue_keywords.append(keyword)
                if not db.keyword.stringFind(name=keyword):
                    if not db.keyword.hasnode(keyword):
                        db.keyword.create(name=keyword)
    
    issue_id = db.issue.create( title=title,
                     status=status, 
                     priority=priority, 
                     score=score, 
                     keyword=keywords, 
                     date=date,
                     author=str(author) )
    db.commit()
    db.close()
    
    return issue_id

def update_issue(issue_id=None, title=None, date=None):
    db = tracker().open('admin')
    
    if date is None:
        date = Date()
    
    issue_keywords = []
    if issue_id is not None:
        db.issue.set(issue_id, title=smart_str(title))
    db.commit()
    db.close()
    return issue_id

def retire_issue(issue_id=None):
    db = tracker().open('admin')
    if issue_id is not None:
        issue = db.issue.getnode(str(issue_id))
    issue.retire()
    db.commit()
    db.close()
    return issue_id

def find_issue(issue_id=None):
    db = tracker().open('admin')
    if issue_id is not None:
        retired = db.issue.is_retired(str(issue_id))
        if retired is True:
            raise ObjectDoesNotExist
        else:
            issue = db.issue.getnode(str(issue_id))
            return issue
    
def create_message(author=None, content='', date='', issue_id=None, issue=None):
    db = tracker().open('admin')
    if date=='':
        date=Date.now()
    node_id = db.msg.create( author=str(author),
                             content=content, 
                             date=date)
    
    if issue is not None or issue_id is not None:
        if issue is None:
            issue=db.issue.getnode(issue_id)
        if issue.messages is not None and issue.messages != []:
            issue.messages +=  [node_id]
        else:
            issue.messages = [ node_id ]
        
    db.commit()
    db.close()
    return node_id

    
def get_user(username=None, id=None, db=None):
    db_opened=False

    if db is None:
        db = tracker().open('admin')
        db_opened = True;

    if username is not None:
        id = db.user.lookup(username)
        userdict = user_to_dict( user=db.user.getnode( id ), db=db)
    elif id is not None:    
        userdict = user_to_dict( user=db.user.getnode( id ))
    elif request.session.has_key('_auth_user_id'):
        userdict = user_to_dict( user=db.user.getnode( session['_auth_user_id'] ), db=db)
    else:
        userdict = user_to_dict( user=db.user.lookup('anonymous')[0] , db=db)

    if db_opened:
        db.close()
    return userdict
   

def get_messages_by_user(username=None, id=None):
    db = tracker().open('admin')
    if username is not None:
        id = db.user.lookup(username)

    message_list = db.msg.find( author=id  )
    return_array = [message_to_dict(id=message_id) for message_id in message_list]
    db.close()
    return return_array

   
def get_message_ids_by_user(username=None, id=None):
    db = tracker().open('admin')
    if username is not None:
        id = db.user.lookup(username)

    message_list = db.msg.find( author={user.id:1}  ) 
    db.close()
    return message_list


def get_issues_by_user(username=None, id=None):
    db = tracker().open('admin')
    if username is not None:
        id = db.user.lookup(username)

    issue_list = db.issue.find( author=id  )
    return_array = [issue_to_dict(issue=None, issue_id=issue_id) for issue_id in issue_list]
    db.close()
    return return_array


def get_issue_ids_by_user(username=None, id=None):
    db = tracker().open('admin')
    if username is not None:
        id = db.user.lookup(username)

    issue_list = db.issue.find( author={user.id:1}  ) 
    db.close()
    return issue_list


def user_to_dict(id=None, username=None, user=None, db=None):
    db_opened=False

    if user is None:
        if db is None:
            db = tracker().open('admin')
            db_opened = True;
        
        if id is not None:
            user = db.user.getnode(id)
        elif username is not None:
            user = db.user.lookup(username)
            
    d = {    'id':user.id,
                'username':user.username,
                'address':user.address,
                'title':user.title,
                'screenname':user.screenname,
                'phone':user.phone,
                'organisation':[],
                'alternate_addresses':user.alternate_addresses,
                'queries':user.queries,
                'roles':user.roles,     # comma-separated string of Role names
                'timezone':user.timezone,
                'language':user.language }

    if db:
        db.close()
    for org in user.organisation:
        d[organisation].append([organisation_to_dict(id=org,db=db)])

    if db_opened:   
        db.close()
    return d

def place_to_dict(place=None, id=None, db=None):
    db_opened=False
    if place is None:
        if id is not None: 
            if db is None:
                db = tracker().open('admin')
                db_opened = True;
            place = db.place.getnode(id)
        else:
            return
    d =  {    'id':place.id,
                'lng':place.lng,
                'lat':place.lat,
                'address':place.address,
                'postalcode':place.postalcode,
                'city':place.city,
                'country':place.country  }

    if db_opened:   
        db.close()

    return d
        
def organisation_to_dict(organisation=None, id=None, db=None):        
    db_opened=False

    if organisation is None:
        if id is not None: 
            if db is None:
                db = tracker().open('admin')
                db_opened = True;
            organisation = db.organisation.getnode(id)
        else:
            return
    d =  {    'id':organisation.id,
              'order':organisation.order,
              'name':organisation.name,
              'logo':organisation.logo,
              'css': organisation.css,
              'homeurl':organisation.homeurl,
              'address':organisation.address,
              'screenname':organisation.screenname,
              'signature':organisation.signature,
              'phone':organisation.phone  }

    if db_opened:   
        db.close()
    return d


def message_to_dict(msg=None, id=None, db=None):        
    db_opened=False
    if db is None:
        db = tracker().open('admin')
        db_opened = True;

    if msg is None:
        if id is not None: 
            msg = db.msg.getnode(id)
        else:
            return

    if msg.date:
        date = str(msg.date)
        smart_date = (smart_date_diff(datetime.datetime(msg.date.year, msg.date.month, 
                                                       msg.date.day, msg.date.hour,
                                                       msg.date.minute, 
                                                       int(msg.date.second))))
    else:
        date = ''
        smart_date = ''

    if msg.author is not None:
        author = db.user.getnode(msg.author)    
        if author.screenname:
            authorname=author.screenname
        else:
            authorname=author.username
        authorlink=author.username
        if author.title:
            authortitle = author.title
        else:
            authortitle = ''
        if author.organisation != []:
            org = db.organisation.getnode(author.organisation[0])
            organisation = {'name':org.name,
                            'logo': org.logo,
                            'css': org.css,
                            'screenname':org.screenname,
                            'signature': org.signature,
                            'linkurl': org.homeurl,
                            'id': org.id  }
            
        else:
            organisation = {'name': None,
                            'logo': None,
                            'css': None,
                            'screenname': None,
                            'signature': None,
                            'linkurl': None,
                            'id': 0   }
    else:
        author = get_user_by_name('anonymous')
        authortitle = ''
        authorname=author.screenname
        organisation = {'name': None,
                            'logo': None,
                            'css': None,
                            'screenname': None,
                            'signature': None,
                            'linkurl': None,
                            'id': 0   }
        
        authorname=author.screenname
        authortitle = author.title
        if author.organisation != []:
            organisation = organisation_to_dict(id=author.organisation[0], db=db)
             

    comment={
             'id': msg.id,
             'author': authorname, 
             'authortitle':authortitle,
             'authorlink':authorlink,
             'organisation': organisation,
             'date': date,
             'smartdate' : smart_date,
             'class': author.organisation is not None and 'org' or '',
             }

    if db.msg.is_retired(msg.id):
        comment.update({'text':_('This message by has been removed by %(actor)s.') % {'actor' : 'administrators'},
                        'class': 'removed' }) 

        if db_opened:
            db.close()
        return comment
        

    comment.update({'text':  msg.content})


    if msg.places != []:
        place = db.place.getnode(msg.places[0])
        comment['point'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id}

    if msg.files != []:
        comment.update({'thumburl':get_image_thumbnail(msg.files[0], 80, 80 ),
                                'imageurl':get_image_thumbnail(msg.files[0], 380, 380) })

#    if len(msg.places)>0:
#        place = db.place.getnode(msg.places[0])
#        comment['point'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address}
#        comment['place'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address}

    if db_opened:   
        db.close()
    return comment



def issue_to_dict(issue, issue_id=None, db=None):
    db_opened=False
    if db is None:
        db = tracker().open('admin')
        db_opened = True;

    if issue is None:
        issue = db.issue.getnode(issue_id)


    if issue.date is not None:
        smart_date = smart_date_diff(datetime.datetime(issue.date.year, issue.date.month, issue.date.day, issue.date.hour,
            issue.date.minute, int(issue.date.second)))
    else:
        smart_date = ''     

    
    if db.issue.is_retired(issue.id):
        rval = {'title':_('This message by has been removed by %(actor)s.') % {'actor' : 'administrators'},
                          'date' : str(issue.date),
                          'smartdate' : smart_date,}
        if db_opened:
            db.close()
        return rval

    
    places = []
    for place_id in issue.places:
        if db.place.hasnode(place_id):
            places.append(db.place.getnode(place_id))
      
    points = []

    for place in places:
        if place.lat and place.lng:
#            print "Appending "+'lat '+  place.lat + ', lng: '+ place.lng
            points.append( {'lat': place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id } )


    
    if issue.author is not None:
        author = db.user.getnode(issue.author)    
        if author.screenname:
            authorname=author.screenname
        else:
            authorname=author.username
        authorlink=author.username

        if author.title:
            authortitle = author.title
        else:
            authortitle = ''
        author_id = author.id
        if author.organisation != []:
            org = db.organisation.getnode(author.organisation[0])
            organisation = {'name':org.name,
                            'logo': org.logo,
                            'css': org.css,
                            'screenname':org.screenname,
                            'signature': org.signature,
                            'linkurl': org.homeurl,
                            'id': org.id  }
        else:
            organisation = {'name': None,
                    'logo': None,
                    'css': None,
                    'screenname': None,
                    'signature': None,
                    'linkurl': None,
                    'id': 0   }

            
    else:
        author = get_user_by_name('anonymous')
        authortitle = ''
        authorname=author.screenname
        authorlink="anonymous"
        author_id = author.id
        organisation = {'name': None,
                            'logo': None,
                            'css': None,
                            'screenname': None,
                            'signature': None,
                            'linkurl': None,
                            'id': 0   }
    rval = {
        'title': issue.title,
        'options': {
            'author_id': int(author_id),
            'author' : authorname,
            'authorlink':authorlink,
            'authortitle': authortitle,
            'organisation' : organisation,
            'date' : str(issue.date),
            'smartdate' : smart_date,
            'points' : points,        
            'score': issue.score,
            'id': issue.id,
            'status': issue.status,
            'icon': {'name':'/images/merkki_sin.png',
                     'activeiconname':'/images/merkki_pun.png',
                     'partlyactiveiconname':'/images/merkki_pun.png',
                     'w': 23,
                     'h': 41,
                     'ax': 5,
                     'ay': 41,
                     },
            'type':'issue',

        },
    }
    if len(issue.keyword) ==0:
        rval['options'].update({ 'link': reverse('report_view', args=[issue.id]) })
    else:
        rval["options"].update({ 'link': reverse('tagged_report_view', args=[db.keyword.getnode(issue.keyword[0]).name, issue.id]) })

    if issue.files != []:
        dummy = 1
        rval['options'].update({'thumburl':get_image_thumbnail(issue.files[0], 80, 80 ),
                                'imageurl':get_image_thumbnail(issue.files[0], 380, 380) })

    
    if len(places)>0:
        if places[0].lat and places[0].lng:
            rval['options'].update ({'onMap': True })
            rval.update ({'point': {'lat': places[0].lat, 
                                               'lon':places[0].lng,
                                               'address':places[0].address,
                                               'id':places[0].id }})
    else:
         rval['options'].update ({'onMap': True })       


    
    if not issue.messages:
        return rval

    comments = []
    last_comment_date = ''
    last_comment_smart_date = ''
    for msg in issue.messages:
        comment_dict = message_to_dict(None,id=msg,db=db)
        if comment_dict.has_key("point"):
#            print "Appending "+'lat '+  place.lat + ', lng: '+ place.lng
            points.append( comment_dict["point"] )

            
        comments.append(comment_dict)
        if comment_dict.has_key('point'):
            rval['options'].update({'onMap':True})
    
    
#        if comment_dict.has_key('point'):
#            rval['options']['points'].append(comment_dict['point'])
    
        if last_comment_date is None or comment_dict['date'] > last_comment_date:
            last_comment_date=  comment_dict['date']
            last_comment_smart_date=  comment_dict['smartdate']
    

    if len(comments)>0:
        commentcount = len(comments)
    else:
        commentcount = "00"
        
    rval['options'].update({
        'last_comment_date' : last_comment_date,
        'last_comment_smartdate' : last_comment_smart_date,                    
        'comments': comments,
        'commentcount': commentcount,
    })
    
    if db_opened:   
        db.close()

    return rval




def message_to_quick_dict(msg=None, id=None, db=None):        
    db_opened=False
    if db is None:
        db = tracker().open('admin')
        db_opened = True;

    if msg is None:
        if id is not None: 
            msg = db.msg.getnode(id)
        else:
            return

#    if msg.date:
#        date = str(msg.date)
#        smart_date = smart_date_diff(datetime.datetime(msg.date.year, msg.date.month, 
#                                                       msg.date.day, msg.date.hour,
#                                                       msg.date.minute, 
#                                                       int(msg.date.second))),
#    else:
#        date = ''
#        smart_date = ''

#    if msg.author is not None:
#        author = db.user.getnode(msg.author)    
#        if author.screenname:
#            authorname=author.screenname
#        else:
#            authorname=author.username
#        if author.title:
#            authortitle = author.title
#        else:
#            authortitle = ''
#        if author.organisation != []:
#            org = db.organisation.getnode(author.organisation[0])
#            organisation = {'name':org.name,
#                            'logo': org.logo,
#                            'css': org.css,
#                            'screenname':org.screenname,
#                            'signature': org.signature,
#                            'linkurl': org.homeurl  }
            
#        else:
#            organisation = {'name': None,
#                            'logo': None,
#                            'css': None,
#                            'screenname': None,
#                            'signature': None,
#                            'linkurl': None   }
#    else:
#        author = get_user_by_name('anonymous')
#        authortitle = ''
#        authorname=author.screenname
#        organisation = {'name': None,
#                            'logo': None,
#                            'css': None,
#                            'screenname': None,
#                            'signature': None,
#                            'linkurl': None   }
#        
#        authorname=author.screenname
#        authortitle = author.title
#        if author.organisation != []:
#            organisation = organisation_to_dict(id=author.organisation[0], db=db)
             

    comment={
             'id': msg.id,
 #            'author': authorname, 
 #            'authortitle':authortitle,
 #            'organisation': organisation,
 #            'date': date,
 #            'smartdate' : smart_date,
 #            'class': author.organisation is not None and 'org' or '',
             }

    if db.msg.is_retired(msg.id):
        comment.update({'text':_('This message by has been removed by %(actor)s.') % {'actor' : 'administrators'},
                        'class': 'removed' }) 

        if db_opened:
            db.close()
        return comment
        

#    comment.update({'text':  msg.content})


    if msg.places != []:
        place = db.place.getnode(msg.places[0])
        comment['point'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id }


    if msg.files != []:
        comment.update({'thumburl':get_image_thumbnail(msg.files[0], 80, 80 ),
                                'imageurl':get_image_thumbnail(msg.files[0], 380, 380) })

    if len(msg.places)>0:
        place = db.place.getnode(msg.places[0])
        comment['point'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id }
        comment['place'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id }

    if db_opened:   
        db.close()
    return comment





def issue_to_quick_dict(issue, issue_id=None, db=None):
    db_opened=False
    if db is None:
        db = tracker().open('admin')
        db_opened = True;

    if issue is None:
        issue = db.issue.getnode(issue_id)


    if issue.date is not None:
        smart_date = smart_date_diff(datetime.datetime(issue.date.year, issue.date.month, issue.date.day, issue.date.hour,
            issue.date.minute, int(issue.date.second)))
    else:
        smart_date = ''     

    
    if db.issue.is_retired(issue.id):
        rval = {'title':_('This message by has been removed by %(actor)s.') % {'actor' : 'administrators'},
                          'date' : str(issue.date),
                          'smartdate' : smart_date,}
        if db_opened:
            db.close()
        return rval

    
    places = []

    for place_id in issue.places:
        if db.place.hasnode(place_id):
            places.append(db.place.getnode(place_id))
      
    points = []

    for place in places:
        if place.lat and place.lng:
#            print "Appending "+'lat '+  place.lat + ', lng: '+ place.lng
            points.append( {'lat': place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id } )


    
#    if issue.author is not None:
#        author = db.user.getnode(issue.author)    
#        if author.screenname:
#            authorname=author.screenname
#        else:
#            authorname=author.username
#        if author.title:
#            authortitle = author.title
#        else:
#            authortitle = ''
#        author_id = author.id
#        if author.organisation != []:
#            org = db.organisation.getnode(author.organisation[0])
#            organisation = {'name':org.name,
#                            'logo': org.logo,
#                            'css': org.css,
#                            'screenname':org.screenname,
#                            'signature': org.signature,
#                            'linkurl': org.homeurl  }
#        else:
#            organisation = {'name': None,
#                    'logo': None,
#                    'css': None,
#                    'screenname': None,
#                    'signature': None,
#                    'linkurl': None   }

            
#    else:
#        author = get_user_by_name('anonymous')
#        authortitle = ''
#        authorname=author.screenname
#        author_id = author.id
#        organisation = {'name': None,
#                            'logo': None,
#                            'css': None,
#                            'screenname': None,
#                            'signature': None,
#                            'linkurl': None   }
    rval = {
        'title': issue.title,
        'points': points,
        'options': {
#            'author_id': int(author_id),
#            'author' : authorname,
#            'authortitle': authortitle,
#            'organisation' : organisation,
            'date' : str(issue.date),
            'smartdate' : smart_date,
            'points' : points,        
            'score': issue.score,
            'id': issue.id,
            'status': issue.status,
            'icon': {'name':'/images/merkki_sin.png',
                     'activeiconname':'/images/merkki_pun.png',
                     'partlyactiveiconname':'/images/merkki_pun.png',
                     'w': 23,
                     'h': 41,
                     'ax': 5,
                     'ay': 41,
                     },
            'type':'issue',

        },
    }
    if len(issue.keyword) ==0:
        rval['options'].update({ 'link': reverse('report_view', args=[issue.id]) })
    else:
        rval['options'].update({ 'link': reverse('tagged_report_view', args=[db.keyword.getnode(issue.keyword[0]).name, issue.id]) })

#    if issue.files != []:
#        dummy = 1
#        rval['options'].update({'thumburl':get_image_thumbnail(issue.files[0], 80, 80 ),
#                                'imageurl':get_image_thumbnail(issue.files[0], 380, 380) })

    
    if len(places)>0:
        if places[0].lat and places[0].lng:
            rval['options'].update ({'onMap': True })
            rval.update ({'point': {'lat': places[0].lat, 
                                               'lon':places[0].lng,
                                               'address':places[0].address }})
    else:
         rval['options'].update ({'onMap': True })       


    
    if not issue.messages:
        if db_opened:   
            db.close()

        return rval

    comments = []
#    last_comment_date = ''
#    last_comment_smart_date = ''
    for msg in issue.messages:
        comment_dict = message_to_quick_dict(None,id=msg,db=db)    
        comments.append(comment_dict)
        if comment_dict.has_key('point'):
            rval['options'].update({'onMap':True})
    
        if comment_dict.has_key('point'):
            rval['options']['points'].append(comment_dict['point'])
            rval['points'].append(comment_dict['point'])
#        if last_comment_date is None or comment_dict['date'] > last_comment_date:
#            last_comment_date=  comment_dict['date']
#            last_comment_smart_date=  comment_dict['smartdate']
    

    commentcount = len(issue.messages)
    
        
    rval['options'].update({
        'commentcount': commentcount,
        'comments': comments,
        
    })
    
    if db_opened:   
        db.close()

    return rval

        
##############################################################

#Slowly get rid of things below this line...

##############################################################

def get_user_id(request=None, username=None):

    if username is not None:
        db = tracker().open('admin')
        if username is not None:
            id = db.user.lookup(username)
        db.close()
        return id
    
#    if not request.session:
#        db = tracker().open('admin')
#        return db.user.lookup('anonymous')[0]
    try:
        profile = request.user.get_profile()
    except Exception:
        db = tracker().open('admin')
        return db.user.lookup('anonymous')[0]
    return profile.roundup_id

def get_user_by_name(username):
    db = tracker().open('admin')
    id = db.user.lookup(username)
    try:
        return db.user.getnode( id )
    except:
        return 



    
def is_anon_user(request):
    db = tracker().open('admin')
    user_id = get_user_id(request)
    anon_ids = db.user.lookup('anonymous')

    if str(user_id) == str(anon_ids[0]):
        return True
    else:
        return False
   
def is_anon_userid(user_id):
    db = tracker().open('admin')
    anon_ids = db.user.lookup('anonymous')

    if str(user_id) == str(anon_ids[0]):
        return True
    else:
        return False 


