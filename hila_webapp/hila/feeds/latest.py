from fillarifeed import FillariFeed
from util.misc_utils import get_popular_messages, get_latest_messages, get_officer_messages,get_tag_decorations, get_latest_issues, get_latest_comments
import datetime


class latest(FillariFeed):

    title = "Fillarikanava latest message updates"
    link = "http://fillarikanava.hel.fi"
    description = "Fillarikanava latest message updates"


    def item_pubdate(self, item):
        dt=item['options']['date']
        return datetime.datetime(int(dt[0:4]), int(dt[5:7]), int(dt[8:10]), int(dt[11:13]), int(dt[14:16]))



    def items(self):

        returnarray = []
        for msg in get_latest_messages(count=7,offset=0,filters=None):
            returnarray.append(msg)
#            returnarray.append({'title': msg['title'],
#        		 'description': msg['title'],
#        		 'date': msg['options']['date'],
#        		 } )

        return returnarray
                


class latest_messages(FillariFeed):

    title = "Fillarikanava latest messages"
    link = "http://fillarikanava.hel.fi"
    description = "Fillarikanava latest messages"


    def item_pubdate(self, item):
        dt=item['options']['date']
        return datetime.datetime(int(dt[0:4]), int(dt[5:7]), int(dt[8:10]), int(dt[11:13]), int(dt[14:16]))



    def items(self):

        returnarray = []
        for msg in get_latest_issues(count=7,offset=0,filters=None):
            returnarray.append(msg)
#            returnarray.append({'title': msg['title'],
#        		 'description': msg['title'],
#        		 'date': msg['options']['date'],
#        		 } )

        return returnarray





class latest_comments(FillariFeed):

    title = "Fillarikanava latest comments"
    link = "http://fillarikanava.hel.fi"
    description = "Fillarikanava latest comments"

    title_template= "fkcommentfeed_title.html"
    description_template = "fkcommentfeed_description.html"
    link_template="fkcommentfeed_link.html"
    extra_kwargs_template="fkcommentfeed_extra.html"



    def items(self):

        returnarray = []
        for msg in get_latest_comments(count=7,offset=0,filters=None):
            returnarray.append(msg)
#            returnarray.append({'title': msg['title'],
#        		 'description': msg['title'],
#        		 'date': msg['options']['date'],
#        		 } )

        return returnarray

