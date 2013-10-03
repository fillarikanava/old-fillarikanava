/**
 * googlemaps.js
 *
 * Funktiokirjasto GoogleMaps-APIn käsittelyyn.
 *
 * @author Janne Nurminen <janne.nurminen ät cs.helsinki.fi>
 */
//<![CDATA[

var lastupdate = 0;
var lastdata = 0;
var lastoffset = 0;
var waiting_text_search = false;




function dotheajaxthing(json_url, keywordstring, view_limit, offset) 
{
		waiting_text_search = false;
		
		if (!keywordstring)
			return;
			
		keywordstring = keywordstring.replace(/^\s+|\s+$/g, '').replace(/\s{2,}/g, ' ');
	
		if (keywordstring == lastdata && offset == lastoffset) {
			return;
		}
		lastdata = keywordstring;
		lastoffset = offset;
		lastupdate += 1;
		
		query = 'seqnum='+ lastupdate;
		if (view_limit) 
		{
			query += '&vlimit='+view_limit;
		}
		if (offset) 
		{
			query += '&offset='+offset;
		}
		query += '&details=yes&keywords='+keywordstring;		
		$.ajax({
			url : (json_url + '?' + query),
			dataType: 'json',
			success: function(data) {
	
//					if (!data[0] || lastupdate != data[0].seqnum) {
				if (!data[0]) {
					return;
				}
				$("#matches").html("Roughly " + data[0]["total_matches"] + " hits. <br>");
				var i = 1;
				while ( i+view_limit < data[0]["total_matches"])
				{
					if (offset+view_limit < i+1 || offset+view_limit > i+view_limit) {
						$("#matches").append(' <a href="javascript:dotheajaxthing(\''+json_url+'\',\''+ keywordstring+'\','+view_limit+','+ (i-1)+');">'+ i + "-" + (i+view_limit-1) +" </a> ");
					}
					else {
						$("#matches").append('<b>'+i + "-" + (i+view_limit-1) + '</b>');
					}
					i+=view_limit;					
				}
				if (i<data[0]["total_matches"])
				{
					if (offset+view_limit < i+1 || offset+view_limit > i+view_limit) {
						$("#matches").append(' <a href="javascript:dotheajaxthing(\''+json_url+'\',\''+ keywordstring+'\','+view_limit+','+ (i-1)+');">'+ i + "-" + (data[0]["total_matches"]) +" </a> ");
					}
					else {
						$("#matches").append('<b>'+i + "-" + (data[0]["total_matches"]) + '</b>');
					}

					i+=view_limit;					
				}
				
				
				$("#matches").append('<ul class="msg_list">');
				$.each(data[1], function(i, issue_data) {
					$("#matches").append(
											searchresulttemplate.process(issue_data) );
					//\n'+
					//						'<h3>' + issue_data.title + '</h3>\n<p>' + 
					//						issue_data.content + '</p>\n</div>');
				});	
				$("#matches").append('</ul>');
				
			}
		});
}

function loadNewMatches (json_url, keywordstring, view_limit, offset)
{
	if (waiting_text_search == true)
		return;
	else
	{
		waiting_text_search = true;
		setTimeout( function() {dotheajaxthing(json_url, keywordstring, view_limit, offset)}, 300 );
	}

}

//]]>