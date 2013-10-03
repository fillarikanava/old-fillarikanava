#!/usr/bin/env python
from django.conf import settings
from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax.handler import ContentHandler 

import re

from roundup import instance
from roundup.date import Date

def add_bug_to_roundup(bug, tracker):
    """Add a roundup bug (dict) to a roundup instance

    :param bug: A dictionary of bug data. Pretty much a plain set of
    property -> value mappings, with the only exception being messages
    which maps to a list of message dictionaries.

    :param tracker: The roundup tracker instance, this is obtained via
    `roundup.instance.open`.

    """
    try:
        print "opening roundup"
        
                # Open up the db and get the user, creating if necessary
        db = tracker.open('admin')
        username = get_roundup_user(db, bug['creator'])
        db.commit()
        db.close()
        
        if len(username) < 1:
            username="anon"

        db = tracker.open(username)

        # Get the issue's properties
        status_id = get_roundup_property(db, 'status', 'unread')
        priority_id = get_roundup_property(db, 'priority', 'normal')

        # Get the users relating to the issue
        # From bugzilla the username is the email, so can use that as a starting point
        creator_id = get_roundup_user(db, bug['creator'])
        assignedto_id = get_roundup_user(db, bug['assignedto'])

        print "adding this bug:"
        print bug

        bug_id = db.issue.create(
            title= bug['title'].encode('utf-8'),
#                product=bug['product'],
#                version=bug['version'],
            status=bug['status'],
            priority=bug['priority'],
            #creator=bug['creator'],
            assignedto=get_roundup_user(db,bug['assignedto'].split("@")[0]),
            #creation=bug['creation'],
            )
        print "still rolling--"
        
        db.commit()
    finally:
        #Ensure the db is always closed no matter what
        db.close()
        print("Roundup db connection closed")

    print("Added issue: %s" % bug_id)
    return bug_id

def add_message_to_roundup(bug_id, message, tracker):
    """Adds the given message to to roundup"""
    try:
        print "opening tracker..."
        
        # Open up the db and get the user, creating if necessary
        db = tracker.open('admin')
        username = get_roundup_user(db, message['creator']).strip()      
        db.commit()
        db.close()




        # Re-open as the user
        db = tracker.open(username)

        # Create the author if not theredemo
        get_roundup_user(db, message['author'])

        print "creating message"

        # Create the message
        message_id = db.msg.create(
            content=message['text'].encode('utf-8'),
            author=message['author'].encode('utf-8'),
            date=Date(message['creation'].replace('T','.').replace('Z','').strip().encode('ascii'))
            )

        # Add the message to the bug
        bug = db.issue.getnode(str(bug_id))
        messages = bug.messages
        messages.append(message_id)
        bug.messages = messages # Force a setattr
        db.commit()
    finally:
        #Ensure the db is always closed no matter what
        db.close()
        print("Roundup db connection closed")

    print("Added message: %s to issue: %s" % (message_id, bug_id))
    return message_id

def add_file_to_roundup(bug_id, filename, content, mimetype, tracker):
    filename = os.path.basename(filename) # ensure there are no directory parts
    try:
        db = tracker.open("admin")

        # Create the file
        file_id = db.file.create(
            content=content,
            name=filename,
            type=mimetype
            )

        #Append the file to the bug
        bug = db.issue.getnode(bug_id)
        files = bug.files
        files.append(file_id)
        bug.files = files

        db.commit()
    finally:
        db.close()
        logger.debug("Closed db connection")

    print("Added file %s to issue %s" % (file_id, bug_id))
    return file_id
    
def get_roundup_property(db, propname, value):
    """Obtains the id of the given property.

    If it doesn't exist it is created.
    """
    klass = db.getclass(propname)
    try:
        result = klass.lookup(value)
    except KeyError:
        result = klass.create(name=value)
    return result

def get_roundup_user(db, email):
    """Find (or create) a user based on their email address

    This assumes everyone has a username which is also their email
    address prefix.
    """
    
    username = email.strip() #email.split("@")[0]
    
    if len(username) < 1:
        username="anon"

    
    try:
        db.user.lookup(username)
    except KeyError:        
        emailaddr=re.sub(r'\s','.',username)+"@invalid.this.email.is"
        print "creating user with "+username + " "+ emailaddr
        db.user.create(username=username, address=emailaddr)
    return username


class IssueHandler(ContentHandler):
    def __init__(self):
        self.variables = {}
        self.tracker = instance.open(settings.TRACKER_HOME)
        self.db = self.tracker.open('admin')
        self.message_array = []

    def startElement(self, name, attrs):
      self.varname= name
      self.variables[name] = attrs.get(name, "")
    def characters (self, ch):
          self.variables[self.varname] += ch
    def endElement(self, name):
      if name == 'suggestion':
          roundup_bug = {}    
          roundup_bug['messages'] = []
          roundup_bug['status'] = 'unread'
          roundup_bug['priority'] = 'normal'
          roundup_bug['title'] = self.variables['title'].strip()
          roundup_bug['assignedto'] = ''        
          roundup_bug['creator'] = self.variables['name'].strip()       
          
          message = {}
          message['text'] = self.variables['text'].strip()
          message['creator'] = self.variables['name'].strip()
          message['author'] = self.variables['name'].strip()          
          message['creation'] = self.variables['created_at'].strip()
          #message['file'] = long_desc.find('thetext').text

          self.message_array.append(message)

          self.bug_id = add_bug_to_roundup(roundup_bug, self.tracker) 
          for messag in self.message_array:
              messag['creation'] = self.variables['created_at'].strip()
              add_message_to_roundup(self.bug_id, messag, self.tracker)

          self.message_array = []

          for k in self.variables.keys():
              print k + ": " + self.variables[k].strip()
              
              
      elif name == 'comment':
          message = {}
          message['text'] = self.variables['comment_text'].strip()
          message['creator'] = self.variables['commenter'].strip()
          message['author'] = self.variables['commenter'].strip()
          #message['file'] = long_desc.find('thetext').text

          self.message_array.append(message)
          
          
      else:
          self.variables[name] = self.variables[name].strip()



    
file = open('suggestions_with_comments.xml', 'r')
parser = make_parser()
parser.setFeature(feature_namespaces, 0)
dh = IssueHandler()
# Tell the parser to use our handler
parser.setContentHandler(dh)
# Parse the input
parser.parse(file)

