from django.core.urlresolvers import reverse
from hila import roundup_utils
from roundup.date import Date
import re
from datetime import datetime


from hila.api.models import Apikey

"""
We have to bring the following from Hepo's widget, using anonymous user and
keyword "Hepo Widget".

> - description / varchar(140)
> - lat / float(10,6)
> - lon / float(10,6)
> - usernickname / varchar(50)
> - address / varchar(255) ts. mysql:n tinytext
> - postalcode / varchar(255)
> - city / varchar(255)
> - country / varchar(255)
"""


def add_message_through_api(request):

    if request.method == 'POST':

        title = request.POST.get('title', None)

        message = request.POST.get('description', None)

        issue_keywords = []

        keywords = request.POST.get('keywords', "")

        apikey = request.POST.get('apikey', None)

        try:
            key = Apikey.objects.filter(key__exact=apikey)[0]
        except IndexError:
            return {'id':-1,'error_description':'invalid API key'}

        # messy messy messy --- TODO:  allow keywords later when they are actually used for something
        keywords = ""

        if key.theme:
            keywords = key.theme.associated_tag

        if len(keywords) > 0:
            keyword_array = re.split(r'[, ;:]', keywords)
            for keyword in keyword_array:
                if len(keyword) >0 :
                    issue_keywords.append(keyword.encode('utf-8'))


        if key.default_user:
            user=key.default_user
        else:
            user="anonymous"

        id=roundup_utils.create_issue(title=title.encode('utf-8'),
                                          keywords=issue_keywords,
                                          author=user)

        if message:
            msg_id = roundup_utils.create_message(author="anonymous",
                                   content=message.encode('utf-8'),
                                   date=Date(),
                                   issue_id = id)
        lat = str(request.POST.get('lat', ""))
        if request.POST.get('lon', "") is not "":
            lng = str(request.POST.get('lon', ""))
        else:
            lng = str(request.POST.get('lng', ""))

        postal = request.POST.get('postalcode', "")
        country = request.POST.get('country', "")
        city = request.POST.get('city', "")
        address = request.POST.get('address', "")


        if postal is None or len(postal) < 1:
            postal = ''
        if address is None or len(address) < 1:
            address = postal

        if len(country)>0 and len(lng)>0 and len(lat)>0 and len(city)>0:
            print "Adding place:"
            place_id = roundup_utils.create_place(lng=lng,
                    lat=lat,
                    address=address.encode('utf-8'),
                    postalcode=postal,
                    city=city.encode('utf-8'),
                    country=country.encode('utf-8'),
                    issue_id=id )
            print "Tried to add... Let's see what we got: place_id: "+place_id
        else:
            try:
                print str(datetime.now()) + "Place attributes bad:" + str(country) + "/" + str(lng)+"/" + str( city) + "/" + str(address)
            except:
                print str(datetime.now()) + "could not print bad map location"


        return {'id':id, 'link': reverse('report_view', args=[id])}
    else:
        return {'id': -1, 'error_description': "request method is not post - Is this true or have we messed up something?"}





def add_comment_through_api():
    return null

