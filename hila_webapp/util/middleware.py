# -*- coding: UTF-8 -*-
'''
Created on 23.3.2009

@author: jsa
'''

class JsonpMiddleware(object):
    """Handles callback-attribute of JSONP."""
    def process_response(self, request, response):
        if response['Content-Type'] == 'application/json':
            callback = request.GET.get('callback', None)
            if callback:
                # wrap inside Javascript method call ('JSON with padding')
                response.content = '%s(%s);' % (callback, response.content)
        return response




class GoogleMapCenterMiddleware(object):
    
    def process_response(self, request, response):

        if request.session.has_key('mapzoomlevel'):
            request.mapzoomlevel= request.session['mapzoomlevel']
        if request.session.has_key('mapcenterlat'):
            request.mapcenterlat = request.session['mapcenterlat']
        if request.session.has_key('mapcenterlng'):
            request.mapcenterlng = request.session['mapcenterlng']
        
    
        return response


class blockCrawlersMiddleware(object):
    def process_request(self, request):
        import re
        if request.META.has_key('HTTP_USER_AGENT'):
            if re.search(r'crawler',request.META['HTTP_USER_AGENT']) and \
                re.search(r'\/api\/',request.get_full_path()):
                HttpResponse("API should not be used by search bots.")




class searchFilterMiddleware(object):
    def process_request(self, request):
        from hila.public.report.models import Theme
        from django.utils.translation import ungettext, ugettext as _
        from django.conf import settings

        if request.session.has_key('filter_from_date'):
            default_from=request.session['filter_from_date']
        else:
            default_from="\"01/01/2009\""
        if request.session.has_key('filter_to_date'):
            default_to=request.session['filter_to_date']
        else:
            default_to=""
        if request.session.has_key('filter_tag'):
            default_tag=request.session['filter_tag']
        else:
            default_tag="none"
        if request.session.has_key('filter_words'):
            default_words=request.session['filter_words']
        else:
            default_words=""


        map_search_filter_js = '<script type="text/javascript" \
                src="'+settings.MEDIA_URL+'js/jquery-date.js"></script>\n'
        map_search_filter_js +=u"<script type=\"text/javascript\"> \
                Date.dayNames = ['sunnuntai', 'maanantai', 'tiistai', \
                 'keskiviikko', 'torstai', 'perjantai', 'lauantai']; \n\
                Date.abbrDayNames = ['su', 'ma', 'ti', 'ke', 'to', 'pe', 'la'];                                           \n\
                Date.monthNames = ['tammikuu', 'helmikuu', 'maaliskuu', 'huhtikuu', 'toukokuu', \
                'kesäkuu', 'heinäkuu', 'elokuu', 'syyskuu', 'lokakuu', 'marraskuu', 'joulukuu'];\n\
                Date.abbrMonthNames = ['T', 'H', 'M', 'H', 'T', 'K', 'H', 'E', 'S', 'L', 'M', 'J'];\n\
</script>"+'<script type="text/javascript" src="'+settings.MEDIA_URL+'js/jquery.datePicker.min-2.1.2.js"></script>\n  \
<script type="text/javascript">\n \
'+u"$.dpText = {    \n \
	TEXT_PREV_YEAR		:	'FI Previous year', \n \
	TEXT_PREV_MONTH		:	'FI Previous month', \n \
	TEXT_NEXT_YEAR		:	'FI Next year',      \n \
	TEXT_NEXT_MONTH		:	'FI Next month',     \n \
	TEXT_CLOSE			:	'FI Close',          \n \
	TEXT_CHOOSE_DATE	:	'"+_("Choose date")+"'     \n \
}; "+'\
$(\'#filtersubmitbutton\').bind(\'click\',function(event) {\n\
					var tabs = $(\'div#front-tabs > div\'); \n\
					tabs.hide();                                \n\
					tabs.filter("#tab-4").show();                 \n\
					$(\'div#front-tabs ul.tab-navi a\').removeClass(\'selected\');\n\
					$(this).addClass(\'selected\');                  \n\
                filterChange = true; refreshData();  searchData(); \n\
                } );   \n                 \
$(\'.tagfilter\').bind(\'click\', function(event) {\n\
                filterChange = true; refreshData();  searchData();   \n   \
                  } );   \n      \
$(function()             \n                                                                          \
{                         \n                                                                          \
	$(\'.date-pick-from\').datePicker({clickInput:true, startDate: "01/03/2009", dateFormat: \'dd.mm.yy\' }).val(new Date('+default_from+').asString()).trigger(\'change\').bind(\
						\'dateSelected\',                           \
						function(e, $td)                           \
						{                                           \
							filterChange = true; refreshData(); searchData(); \
						}                                            \
					);\n        \
	$(\'.date-pick-to\').datePicker({clickInput:true, startDate: "01/03/2009", dateFormat: \'dd.mm.yy\' }).val(new Date('+ default_to+').asString()).trigger(\'change\').bind(\
						\'dateSelected\',                           \
						function(e, $td)                           \
						{                                           \
							filterChange = true; refreshData(); searchData();  \
						}                                            \
					);  \n         \
})     \n                                                                                                 \
var characterCode;  \
                                                                          \
$(\'#keywordfilter\').bind(\'keyup\', function(e){\n\
if(e && e.which){   \
e = e;                                                                       \
characterCode = e.which; \
}                                                             \
else{                                                          \
e = event;                                                       \
characterCode = e.keyCode;  \
}                                                                              \
                if (characterCode == 13) {filterChange = true; refreshData(); searchData(); }   \n                 \
                  } );   \n      \
</script>\n'


        map_search_filter ='<div id="searchFilters"> \
<p>'+_("Search")+'                              \
	<br>                                 \
	                                                            \
		<input type="text" id="keywordfilter" name="keywordfilter" size="20" value="'+default_words+'">                 \
<input type="button" name="button" class="refreshButton" id="filtersubmitbutton" value="'+_("Search")+'" /> \
            \
	<br>                                                                      \
	'+_("Filter by time:") +'                                                                   \
	'+_("from [preposition]") +'                                                                        \
		<input name="date_from" id="date_from_filter" class="date-pick-from" size="10" /> \
	'+_("from [postposition]") +'                                                                        \
	'+_("to [preposition]") +'                                                                        \
		<input name="date_to" id="date_to_filter" class="date-pick-to" size="10" />        \
	'+_("to [postposition]") +'                                                                        \
	<br>                                                                              \
		                                                                               \
	'+_('Filter by questionnaires:')+'<br/>\
        <input type="radio" class="tagfilter" name="tagfilter" value="none"'
        if "none" == default_tag:
            map_search_filter +=' checked=checked'
        map_search_filter +='>'+ _('All')+'<br>'


        for tag in Theme.objects.filter(searchable__exact=True):
            map_search_filter +=' \
        <input type="radio" class="tagfilter" name="tagfilter" value="'+tag.name+'"'
            if tag.name == default_tag:
                map_search_filter +=' checked=checked'
            map_search_filter +='>'+ _(tag.description)+'<br>'


        map_search_filter += '</div>'

        request.session['map_search_filter'] = map_search_filter
        request.session['map_search_filter_js'] = map_search_filter_js
        return None
