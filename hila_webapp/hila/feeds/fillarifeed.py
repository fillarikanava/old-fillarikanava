from django.contrib.syndication.feeds import Feed
import datetime
from django.utils.feedgenerator import Rss201rev2Feed

class ExtendedRSSFeed(Rss201rev2Feed):
    """
    Create a type of RSS feed that has content:encoded elements.
    """
    """
    def root_attributes(self):
        attrs = super(ExtendedRSSFeed, self).root_attributes()
        attrs['georss:point'] = 'http://www.georss.org/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('georss:point', item['georss_point'])
    """

    def rss_attributes(self):
        attrs = super(ExtendedRSSFeed, self).rss_attributes()
        attrs['xmlns:georss'] = 'http://www.georss.org/'
        return attrs

    def add_item_elements(self, handler, item):
        """Callback to add elements to each item (item/entry) element."""
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)

        handler.addQuickElement(u"georss:point",  item['georss:point'])





class FillariFeed(Feed):

    feed_type = ExtendedRSSFeed

    title = "Fillarikanava site news"
    link = "/"
    description = "Updates on changes on Fillarikanava"
    author = "community"
    item_author_name = ""
    item_author_link = ""
    item_georss_point = ""

    title_template= "fkfeed_title.html"
    description_template = "fkfeed_description.html"
    link_template="fkfeed_link.html"
    extra_kwargs_template="fkfeed_extra.html"

    def feed_extra_kwargs(self, obj):
        return {'georss:point': ""}

    def item_extra_kwargs(self, item):
        return {'georss:point': self.item_georss_point(item)}


    def item_georss_point(self, item):
        if item.has_key('point'):
            if item['point'].has_key('lon'):
                return item['point']['lat'] +" " +item['point']['lon']
            else:
                return item['point']['lat'] +" " +item['point']['lng']
        else:
            return ""

    """
    Very generously provide functionality for both messages and comments:
        """

    def item_link(self, item):
        if item.has_key('options'):
            return item['options']['link']
        else:
            print item
            return "http://fillarikanava.hel.fi/r/"+item['parent_id']+"#comment_"+item['id']

    def item_author_name(self,item):
        if item.has_key('options'):
            return item['options']['author']
        else:
            return item['author']

    def item_author_link(self,item):
        if item.has_key('options'):
            return "http://fillarikanava.hel.fi/user/"+item['options']['authorlink']
        else:
            return "http://fillarikanava.hel.fi/user/"+item['authorlink']


    def guid(self, item):
        if item.has_key('options'):
            return item['options']['link']
        else:
            return "http://fillarikanava.hel.fi/r/"+item['parent_id']+"#comment_"+item['id']

    def link(self):
       return "http://fillarikanava.hel.fi/"



    def item_pubdate(self, item):
        if item.has_key('options'):
            dt=item['options']['date']
        else:
            dt=item['date']
        return datetime.datetime(int(dt[0:4]), int(dt[5:7]), int(dt[8:10]), int(dt[11:13]), int(dt[14:16]))


                
