#!/usr/bin/env python
from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax.handler import ContentHandler 

import re

from roundup import instance
from roundup.date import Date



class IssueHandler(ContentHandler):
    def __init__(self):
        self.variables = {}
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
          roundup_bug['title'] = re.sub(r'\'', '`', self.variables['title'].strip())
          roundup_bug['assignedto'] = ''        
          roundup_bug['creator'] = self.variables['name'].strip()       
          roundup_bug['author'] = self.variables['name'].strip()
          roundup_bug['date'] = re.sub(r'Z', '', re.sub(r'T','.', self.variables['created_at'].strip()))       
          roundup_bug['created'] = self.variables['created_at'].strip()
          
          message = {}
          message['text'] = re.sub(r'\'', '`', self.variables['text'].strip())
          message['creator'] = self.variables['name'].strip()
          message['author'] = self.variables['name'].strip()          
          message['creation'] = self.variables['created_at'].strip()
          #message['file'] = long_desc.find('thetext').text

          self.message_array.append(message)

          roundup_bug['messages_'] = self.message_array

#          self.bug_id = add_bug_to_roundup(roundup_bug, self.tracker) 
          
          
          
#          for messag in self.message_array:
#              messag['creation'] = self.variables['created_at'].strip()
#              add_message_to_roundup(self.bug_id, messag, self.tracker)

          issues.append(roundup_bug)

          self.message_array = []

#          for k in self.variables.keys():
#              print k + ": " + self.variables[k].strip()
              
              
      elif name == 'comment':
          message = {}
          message['text'] = self.variables['comment_text'].strip()
          message['creator'] = self.variables['commenter'].strip()
          message['author'] = self.variables['commenter'].strip()
          #message['date'] = self.variables['created_at'].strip()

          #message['file'] = long_desc.find('thetext').text

          self.message_array.append(message)
          
          
      else:
          self.variables[name] = self.variables[name].strip()


issues = []
usercounter = 0
users = {'anonymous':0}

    
file = open('suggestions_with_comments.xml', 'r')
parser = make_parser()
parser.setFeature(feature_namespaces, 0)
dh = IssueHandler()
# Tell the parser to use our handler
parser.setContentHandler(dh)
# Parse the input
parser.parse(file)

print 'usercounter = 0\n\
users = {\'anonymous\':anon_id}\n\
'


for bug in issues:

    counter = 0
    print 'message_ids = []'
    
    for message in bug['messages_']:

 #       message_id = db.msg.create(
 #               content=message['text'].encode('utf-8'),
 #               author=message['author'].encode('utf-8'),
#                date=Date(message['creation'].replace('T','.').replace('Z','').strip().encode('ascii'))
#                )
        

        if len(message['author'].encode('utf-8')) < 1:
            username = 'anonymous'
        else:
            username = message['author'].encode('utf-8')
    
#        if counter != 0:
        counter += 1
    
        if users.has_key(username):
            print 'id = msg.create(author=users["' + username + '"],\\' 
        else:
            users[username] = 0
            print 'users["' + username + '"] = db.user.create(username="' + username +'",screenname="' + username +'", address="invalid@email"+ str(usercounter) +".no", organisation=[\'Kaupunkifillari uservoice user\'])'
            print 'usercounter += 1'
            print 'id = msg.create(author=users["' + username + '"],\\' 
    
        print '      content=u\'' + re.sub(r'\'', r"\\'", re.sub(r'\n', r'\\\n', message['text'].encode('utf-8'))) + '\'.encode(\'utf-8\'))'

        print 'message_ids.append (str(id))'
    
    print 'id=db.issue.create(title=u\'' + bug['title'] + '\'.encode(\'utf-8\'),\\'
    print                    'date=Date(\'' + bug['date'] + '\'),\\'
    print                    'author=u\'' + bug['author'] + '\'.encode(\'utf-8\'),\\'
    print '                   status=\'2\', priority=\'3\', messages=message_ids, score=\'2\' )'
    print 
#    print 'db.issue.set(id, creation=\''+ re.sub(r'T', r'.', re.sub(r'Z', '',bug['created'] ))  +'\')'
#    print 'db.issue.set(id, creator=users[\''+ bug['creator'] +'\'])'
 



