


var newicon = new GIcon();
newicon.image =  MEDIA_URL  + "/images/uusi_pointer.png";
newicon.shadow =  MEDIA_URL + "/images/uusi_pointer_shadow.png";
newicon.iconSize = new GSize(50, 50);
newicon.shadowSize = new GSize(40, 50);
newicon.iconAnchor = new GPoint(0, 54);
newicon.infoWindowAnchor = new GPoint(20, 18);



/* 
 *
 *  Initialise "add new" button:
 */


function newButtonInit()
{	

	if (newMarker && screenState == 'create')
	{

		document.write('<div id="AddMessageButtonDiv">'+
				'<button type="button" onClick="javascript:newButtonCancelClick()">'+
				msg_cancel +
				'</button></div>'); 
		var ButtonDiv=document.getElementById("AddMessageButtonDiv"); 
		var pos = new GControlPosition(G_ANCHOR_TOP_RIGHT, new GSize(5,5)); 
		pos.apply(ButtonDiv); 
		map.getContainer().appendChild(ButtonDiv);
		
		if ($("#newmarkerbutton")) $("#newmarkerbutton").hide('slow');
		if ($("#newmarkerform")) $("#newmarkerform").show('slow');
		
		$("#id_issueaddress").bind('keyup', locationFunc);
	}
	else if (screenState == 'view' || screenState == 'front' || screenState == 'create')
	{

		
		document.write('<div id="AddMessageButtonDiv">'+ 
				'<button type="button" onClick="javascript:newButtonClick()">'+
				msg_addbutton +
				'</button></div>'); 
		var ButtonDiv=document.getElementById("AddMessageButtonDiv"); 
		var pos = new GControlPosition(G_ANCHOR_TOP_RIGHT, new GSize(5,5)); 
		pos.apply(ButtonDiv); 
		map.getContainer().appendChild(ButtonDiv);
		

	}

}
/*  What to do when "add new" button clicked: */
var mouseMove, buttonClick, mapClick;
var waiting_geocode = false ;

function locationFunc() {
	
	if (waiting_geocode == true)
		return;
	else
	{
		waiting_geocode = false;

		setTimeout(function() { 
			waiting_geocode = false;
			var this_address = $("#id_issueaddress").val() + " , Helsinki, Finland";
			var geocoder = new GClientGeocoder();
			geocoder.getLocations( this_address, function(response) {

				this_location = showIssueLocation(response);
				if (this_location == 'aaa') {
					$("#addresswarning").html('<span  style="background-color:#FF0000">'+
							msg_address_not_found + 
							'<br>'+
							this_address + 
							'</span>');
				}
				else
				{
					dog = false;

					if (mouseMove != null) {GEvent.removeListener(mouseMove); mouseMove = null}
					if (mapClick != null) {GEvent.removeListener(mapClick); mapClick = null}
					if (newMarker)
						map.removeOverlay(newMarker);
					
					mouseMove = null;
					mapClick = null;

					$("#addresswarning").html('  ');
					newMarker = new GMarker(this_location,{draggable:true, autoPan:false, icon:newicon, clickable:false } );

					map.addOverlay(newMarker);
					map.setCenter(this_location);
					GEvent.addListener(newMarker, 'dragend', function(markerPoint){
						{
							geocoder.getLocations(markerPoint, showIssueAddress);
						}
					});
				}
			});
			}, 1000);
	
	}

}

function newButtonClick(thingy)
{

	if (screenState == 'view' || screenState == 'front' || screenState == 'create')
	{			
		if(newMarker)
		{
			map.removeOverlay(newMarker);
		}

		$("#AddMessageButtonDiv").html('<div id="AddMessageButtonDiv">'+ 
				'<button type="button" onClick="javascript:newButtonCancelClick()">'+
				msg_cancel +
				'</button></div>'); 
//				'<a class="marker" href="javascript:newButtonCancelClick()">'+
//				'<img src="{{ MEDIA_URL }}/images/uusi_btn_down.png" border=0 alt="{% trans "Click here and add a place on the map!" %}">'+
//				'</a></div>'); 

		var dog = true;
		var noMore = false;

		if ($("#newmarkerbutton")) $("#newmarkerbutton").hide('slow');
		if ($("#newmarkerform")) 
		{
			$("#newmarkerform").show('slow');			
			$("#id_issueaddress").bind('keyup', locationFunc);
		}		
		
		mouseMove = GEvent.addListener(map, 'mousemove', function(cursorPoint)
		{
			if(!noMore){

				newMarker = new GMarker(cursorPoint,{draggable:true, autoPan:false, icon:newicon, clickable:false });
				map.addOverlay(newMarker);

				noMore = true;
				// This function deletes the marker when dragged outside map

				GEvent.addListener(newMarker, 'drag', function(markerPoint){
					if(!map.getBounds().containsLatLng(markerPoint)){
						map.removeOverlay(newMarker);
					}
				});
				GEvent.addListener(newMarker, 'dragend', function(markerPoint){
					{
						geocoder.getLocations(markerPoint, showIssueAddress);
					}
				});
			}
			if(dog){
				newMarker.setLatLng(cursorPoint);
			}
		});

		mapClick = GEvent.addListener(map, 'click', function(overlay, point)
			{
				dog = false;
				// 'mousemove' event listener is deleted to save resources
				GEvent.removeListener(mouseMove);
				GEvent.removeListener(mapClick);
				if (screenState == 'view' || 'create' == screenState ) {
					geocoder.getLocations(point, showIssueAddress);
				}
				else if (screenState == 'front') {
					window.document.location.href = create_url + '?lat='+point.y+'&lng='+point.x;
				}

			}
		);
	}
}


/*  What to do when a click occurs in "add new" state: */

function newButtonCancelClick()
{	
	{
		if (mouseMove != null) GEvent.removeListener(mouseMove);
		if (mapClick != null) GEvent.removeListener(mapClick);
		map.removeOverlay(newMarker);
		
		mouseMove = null;
		mapClick = null;

		showIssueAddress('zero');
		
		$("#newmarkerbutton").show('slow');
		$("#newmarkerform").hide('slow');			

		$("#AddMessageButtonDiv").html('<div id="AddMessageButtonDiv">'+ 
				'<button type="button" onClick="javascript:newButtonClick()">'+
				msg_addbutton +
				'</button></div>'); 

//				'<a class="marker" href="javascript:newButtonClick()">'+
//				'<img src="{{ MEDIA_URL }}/images/uusi_btn.png" border=0 alt="{% trans "Click here and add a place on the map!" %}">'+
//				'</a></div>'); 

	}
}
