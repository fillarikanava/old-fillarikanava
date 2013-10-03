/**
 * googlemaps.js
 *
 * Funktiokirjasto GoogleMaps-APIn käsittelyyn.
 *
 * @author Janne Nurminen <janne.nurminen ät cs.helsinki.fi>
 */
//<![CDATA[

var lastupdate = 0
var lastdata = 0

var waiting_text_search = false

function loadNewMatches (json_url, keywordstring, view_limit, offset) {

	if (waiting_text_search == true)
		return;
	else
	{
		waiting_text_search = true;
		setTimeout(function() { 
			waiting_text_search = false;
			
			keywordstring = keywordstring.replace(/^\s+|\s+$/g, '').replace(/\s{2,}/g, ' ');
		
			if (keywordstring == lastdata) {
				return;
			}
			lastdata = keywordstring;
			
//			lastupdate += 1;
			
			query = 'seqnum='+ lastupdate;
			if (view_limit) 
			{
				query += '&vlimit='+view_limit;
			}
			if (offset) 
			{
				query += '&offset='+offset;
			}
			query += '&keywords='+keywordstring;		
			
			$.ajax({
				url : (json_url + '?' + query),
				dataType: 'json',
				success: function(data) {
		
//					if (!data[0] || lastupdate != data[0].seqnum) {
					if (!data[0]) {
						return;
					}
					$("#matches").html('');
					$.each(data, function(i, issue_data) {
						$("#matches").append('\n<div class="rtsearchresultwrapper">\n'+
												'<h3>' + issue_data.title + '</h3>\n<p>' + 
												issue_data.content + '</p>\n</div>');
					});	
				}
			});
		}, 300)
	}
}



//]]>