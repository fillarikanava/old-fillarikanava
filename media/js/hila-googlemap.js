/**
 * hila-googlemaps.js
 *
 * Funktiokirjasto GoogleMaps-APIn käsittelyyn.
 *
 */

/*global $, MEDIA_URL, document, jstCustomModifiers */

// gMaps globals
/*global GBrowserIsCompatible, GClientGeocoder, GEvent, GIcon, GLatLng, GMap2, GMarker, GPoint, GSize, GSmallMapControl */

var map;
var geocoder;
//var zoomlevel = 11;
//var centerLat = 60.172225;
//var centerLng = 24.941926;
var icon;
var this_issue_markers = [];

//var outerBounds = new GLatLngBounds();

var outerSW; 
var outerNE;

var clusterStack = [];
var superStack = [];
                         
                         

function issue_highlight(id) {

	$.each(superStack, function(count, id_and_markers) {
		if (id_and_markers[0] == id) {
			$.each(id_and_markers[1], function (count, marker) {
				marker.setImage(MEDIA_URL +'/images/merkki_pun.png');
			});
		}
	});
	
}


function stop_issue_highlight(id) {

	$.each(superStack, function(count, id_and_markers) {
		if (id_and_markers[0] == id) {
			$.each(id_and_markers[1], function (count, marker) {
				marker.setImage(MEDIA_URL +'/images/merkki_sin.png');
			});
		}
	});
	
}                        
                         
function showIssue(issue_data, template, previewtemplate, clustertemplate) 
{

	var icon = new GIcon();
	icon.image = MEDIA_URL + issue_data.options.icon.name; 
	//'images/merkki_' +
	//({4: 'pun', 5: 'sin'}[5] || 'kel') +
	//'.png';
	icon.shadow = MEDIA_URL + 'images/pointer/cycle-shadow.png';
	icon.iconSize = new GSize(issue_data.options.icon.w, issue_data.options.icon.h);
	icon.shadowSize = new GSize(40, 41);
	icon.iconAnchor = new GPoint(issue_data.options.icon.ax, issue_data.options.icon.ay);

	icon.infoWindowAnchor = new GPoint(110, 18);

	if (clustertemplate && issue_data.options.type == "cluster") 
	{
		var point = new GLatLng(issue_data.point.lat, issue_data.point.lon);
		var marker = new GMarker(point, icon);
		map.addOverlay(marker);		
		GEvent.addListener(marker, "click", function() {
			if( map.getExtInfoWindow() != null ){
				map.closeExtInfoWindow();
			}
			issue_data._MODIFIERS = Hila.jst.jstCustomModifiers;
			marker.openExtInfoWindow(map,
              "simple_example_window",
              clustertemplate.process(issue_data),
              {beakOffset: 2}
            );
		});
		GEvent.addListener(marker, "mouseover", function() {
				marker.setImage(MEDIA_URL + issue_data.options.icon.activeiconname);
		});
	}
	else 
	{
		var markerstack = new Array();
	
		if (issue_data.point) {
	
			var point = new GLatLng(issue_data.point.lat,issue_data.point.lon);
			var issuemarker = new GMarker(point, icon);
	
			markerstack.push(issuemarker);
			map.addOverlay(issuemarker);
	
			if (previewtemplate) 
			{
				GEvent.addListener(issuemarker, "click", function() {
					if( map.getExtInfoWindow() != null ){
						map.closeExtInfoWindow();
					}
					issue_data._MODIFIERS = Hila.jst.jstCustomModifiers;
					issuemarker.openExtInfoWindow(map,
							"simple_example_window",
							previewtemplate.process(issue_data),
							{beakOffset: 2}
					);
				});
				GEvent.addListener(issuemarker, "mouseover", function() {
					$.each(markerstack, function(count, the_marker) {
						the_marker.setImage(MEDIA_URL + issue_data.options.icon.activeiconname);
					});
				});
				GEvent.addListener(issuemarker, "mouseout", function() {
					$.each(markerstack, function(count, the_marker) {
						the_marker.setImage(MEDIA_URL +issue_data.options.icon.name);
					});
				});
	
			}

			
		}	
		if (issue_data.options.comments)
		{
			$.each(issue_data.options.comments, function(count, i) {
				if (i.point) 
				{
					
					var point = new GLatLng(i.point.lat,i.point.lng);
					var marker = new GMarker(point, icon);
		
					map.addOverlay(marker);
		
					markerstack.push(marker);
		
					var new_i = {}
					for (var key in issue_data) {
						new_i[key] = issue_data[key]; 
					}
					for (var key in i) {
						new_i[key] = i[key]; 
					}
					if (previewtemplate) 
					{
						GEvent.addListener(marker, "click", function() {
							if( map.getExtInfoWindow() != null ){
								map.closeExtInfoWindow();
							}
							issue_data._MODIFIERS = Hila.jst.jstCustomModifiers;
							marker.openExtInfoWindow(map,
									"simple_example_window",
									previewtemplate.process( new_i ),
									{beakOffset: 2}
							);
						});
						GEvent.addListener(marker, "mouseover", function() {
							$.each(markerstack, function(count, the_marker) {
								the_marker.setImage(MEDIA_URL +'/images/merkki_pun.png');
							});
						});
						GEvent.addListener(marker, "mouseout", function() {
							$.each(markerstack, function(count, the_marker) {
								the_marker.setImage(MEDIA_URL +issue_data.options.icon.name);
							});
						});
					}
		
					if (document.getElementById("GUseMapCB")) {
						document.verifyform.GUseMapCB.checked = true;
					}
				}
		
			});
	
		}
		superStack.push([issue_data.options.id, markerstack]);
	}
}
function loadNewEvents(json_url, template, previewtemplate, clustertemplate, data) {

	// I wouldn't want to load the maps with every 1 pixel drag.
	// This check does not seem to work - let's fix it when we have time. rk. 

	var sw = map.getBounds().getSouthWest();
	var ne = map.getBounds().getNorthEast();

	

	var dx = ne.lng() - sw.lng();
	var dy = ne.lat() - sw.lat();

	
	var d = data || {};
	$.extend(d, {
			x1: sw.lng() - 0.5 * dx,
			y1: sw.lat() - 0.5 * dy,
			x2: ne.lng() + 0.5 * dx,
			y2: ne.lat() + 0.5 * dy,
			zoomlevel: map.getZoom()
		});

	if ( outerSW && outerNE &&
			ne.lng() < outerNE.lng() && ne.lat() < outerNE.lat() && 
			sw.lng() > outerSW.lng() && sw.lat() > outerSW.lat())
	{
		$.extend(d, {
			nosearch: 1
		});
		$.ajax({
			url : json_url,
			data: d,
			dataType: 'json',
			success: function() {}
		});
	}
	else
	{

		
//		outerBounds = new GLatLngBounds(new GLatLng(d.x1, d.y1), new GLatLng(d.x2, d.y2) )

		outerSW = new GLatLng(d.y1, d.x1);
		outerNE = new GLatLng(d.y2, d.x2 );
		
		$.ajax({
			url : json_url,
			data: d,
			dataType: 'json',
			success: function(data) {
				map.clearOverlays();
				// if the user is placing a new point on the map, it must be reloaded after clearing.
				if (newMarker != null)	{ map.addOverlay(newMarker); }			

				$.each (this_issue_markers, function(i, issueMarker) {
					map.addOverlay(issueMarker);
				});

				$.each(data, function(i, issue_data) {
					showIssue(issue_data, template, previewtemplate, clustertemplate);
				});	

				
			}
		});
	}
}


function load(refreshFun, centerLat, centerLng, zoomlevel) {

	if (GBrowserIsCompatible()) {
		var icon = new GIcon();
		icon.image = MEDIA_URL + "images/icons/google_map_pointer_cycle.png";
		icon.shadow = MEDIA_URL + "images/icons/google_map_pointer_cycle_shadow.png";
		icon.iconSize = new GSize(50, 50);
		icon.shadowSize = new GSize(40, 50);
		icon.iconAnchor = new GPoint(10, 46);
		icon.infoWindowAnchor = new GPoint(20, 18);

		map = new GMap2(document.getElementById("map"));
		map.addControl(new GSmallMapControl());
		map.setCenter(new GLatLng(centerLat, centerLng), zoomlevel);

		GEvent.addListener(map, "moveend", function() { refreshFun(); });

		geocoder = new GClientGeocoder();
		geocoder.setBaseCountryCode("fi");
	}
}

function addAddressToMap(response) {
	//	map.clearOverlays();
	if (!response || response.Status.code != 200) {
		// alert("Pahoittelut, osoitteen hakeminen ei onnistunut.");
		if(document.getElementById("GUseMapCB")) {
			document.verifyform.GUseMapCB.checked = false;
			document.verifyform.GUseMapCB.disabled = true;
		}
	} else {
		var place = response.Placemark[0];
		var point = new GLatLng(place.Point.coordinates[0],
				place.Point.coordinates[1]);
//		map.setCenter(point, zoomlevel);
		if(zoomlevel >= 10) {
			var marker = new GMarker(point, icon);
			map.addOverlay(marker);

			if(document.getElementById("GUseMapCB")) {
				document.verifyform.GUseMapCB.checked = true;
			}
		}
	}
}


var images = [
 "http://maps.google.com/mapfiles/marker.png",
 "http://maps.google.com/mapfiles/dd-start.png",
 "http://maps.google.com/mapfiles/dd-end.png"
];


var newMarker;

function putFirstMarker(imageInd,lat,lng){
	
//	var dog = true;
//	var noMore = false;
//	var hasOverlay = false;
	var geocoder = new GClientGeocoder();
	
	
	var icon = new GIcon();
	icon.image = MEDIA_URL + 'images/merkki_' +
	({4: 'pun', 5: 'sin'}[5] || 'kel') +
	'.png';
	icon.shadow = MEDIA_URL + 'images/pointer/cycle-shadow.png';
	icon.iconSize = new GSize(40, 50);
	icon.shadowSize = new GSize(40, 50);
	icon.iconAnchor = new GPoint(10, 46);
	icon.infoWindowAnchor = new GPoint(20, 18);
	
	var newicon = new GIcon();
	newicon.image =  MEDIA_URL  + "/images/uusi_pointer.png";
	newicon.shadow =  MEDIA_URL + "/images/uusi_pointer_shadow.png";
	newicon.iconSize = new GSize(50, 50);
	newicon.shadowSize = new GSize(40, 50);
	newicon.iconAnchor = new GPoint(0, 54);
	newicon.infoWindowAnchor = new GPoint(20, 18);
	
	if (lat && lng)
	{
		if (newMarker) {
			map.removeOverlay(newMarker);
		}
		point = new GLatLng(lat,lng)
		
		newMarker = new GMarker(point,{draggable:true, autoPan:true, icon:newicon});
		map.addOverlay(newMarker);
		
		newMarker.setImage(newicon);

		var bounds = new GLatLngBounds();
		bounds.extend(point);
		if (!bounds.isEmpty()){
			map.setZoom(map.getBoundsZoomLevel(bounds)-2);
			map.setCenter(bounds.getCenter());
		}

		geocoder.getLocations(point, showIssueAddress);

		hasOverlay = true;

		// This function deletes the marker when dragged outside map
		GEvent.addListener(newMarker, 'drag', function(markerPoint){
			if(!map.getBounds().containsLatLng(markerPoint)){
				map.removeOverlay(newMarker);
				hasOverlay = false;
			}	 
		});
		GEvent.addListener(newMarker, 'dragend', function(markerPoint){
			{	
				// Would centering be desired behaviour?
				// map.setCenter(markerPoint);
				if (hasOverlay) {
					geocoder.getLocations(markerPoint, showIssueAddress); 
				}
			}
		});
	}
}




function followAndPutMarker(imageInd, func, cancelimage) {

	
//	$("#AddMessageButtonDiv").html('<div id="AddMessageButtonDiv">'+ '<a class="marker" href="javascript:followAndPutMarker(0, onClickFunction)">'+cancelimage+'</a></div>');
//	map.getContainer().removeChild(ButtonDiv);

	
	if(newMarker){
		map.removeOverlay(newMarker);
	}

	var dog = true;
	var noMore = false;

	$("#newmarkerbutton").hide('slow');
	$("#newmarkerform").show('slow');
	
	var newicon = new GIcon();
	newicon.image =  MEDIA_URL  + "/images/uusi_pointer.png";
	newicon.shadow =  MEDIA_URL + "/images/uusi_pointer_shadow.png";
	newicon.iconSize = new GSize(50, 50);
	newicon.shadowSize = new GSize(40, 50);
	newicon.iconAnchor = new GPoint(0, 54);
	newicon.infoWindowAnchor = new GPoint(20, 18);
	
	var mouseMove = GEvent.addListener(map, 'mousemove', function(cursorPoint){
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
	var mapClick = GEvent.addListener(map, 'click', function(overlay, point){
		if (func) {
			func(point);
		}
		else 
		{
			dog = false;
			// 'mousemove' event listener is deleted to save resources
			GEvent.removeListener(mouseMove);
			GEvent.removeListener(mapClick);

			geocoder.getLocations(point, showIssueAddress);
		}
	});	
}


function showIssueAddress(response) {

	if (response == 'zero') {
		$("#issueaddress").html('');
		$("#id_issueaddress").val('') ;
		
		$("#id_issuepostal").val('') ;
		$("#id_issuecity").val('') ;
		$("#id_issuecountry").val('') ;
		$("#id_issuelat").val(''); 
		$("#id_issuelng").val('');
	
		 $("#id_issueaddress").trigger('change');
		
		
	}
	else if (!response || response.Status.code != 200) {
		$("#issueaddress").html(
				"Status Code:" + response.Status.code );
	} else {
		place = response.Placemark[0];
		point = new GLatLng(place.Point.coordinates[1],place.Point.coordinates[0]);
		marker = new GMarker(point);
		
		if (place.address)
			$("#issueaddress").html(
				'<b>orig latlng:</b>' + response.name + '<br/>' + 
//				'<b>latlng:</b>' + place.Point.coordinates[1] + "," + place.Point.coordinates[0] + '<br>' +
//				'<b>Status Code:</b>' + response.Status.code + '<br>' +
//				'<b>Status Request:</b>' + response.Status.request + '<br>' +
				'<b>Address:</b>' + place.address + '<br>' 
//				+
//				'<b>Accuracy:</b>' + place.AddressDetails.Accuracy + '<br>' +
//				'<b>Country code:</b> ' + place.AddressDetails.Country.CountryNameCode
				);
		else 
			$("#issueaddress").html(place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.PostalCode.PostalCodeNumber 
					+ " " 
					+ place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName);
		
		if (place.address)
			$("#id_issueaddress").val( place.address.split(',')[0] ) ;
		else
			$("#id_issueaddress").val(place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.PostalCode.PostalCodeNumber 
					+ " " 
					+ place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName);
//		var postalAddress = place.address.split(',')[1].replace(/^\s+|\s+$/g, '') ;

		$("#id_issuepostal").val( place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.PostalCode.PostalCodeNumber ) ;
		$("#id_issuecity").val(   place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName) ;

		$("#id_issuecountry").val(   place.AddressDetails.Country.CountryName) ;

		$("#id_issuelat").val( response.name.split(",")[0] ); 
		$("#id_issuelng").val( response.name.split(",")[1] );
	
		 $("#id_issueaddress").trigger('change');
		
		
		 return point;
	}
}

function showIssueLocation(response) {
	if (response == 'zero') {
		$("#issueaddress").html('');
		$("#id_issueaddress").val('') ;
		
		$("#id_issuepostal").val('') ;
		$("#id_issuecity").val('') ;
		$("#id_issuecountry").val('') ;
		$("#id_issuelat").val(''); 
		$("#id_issuelng").val('');
	
		 $("#id_issueaddress").trigger('change');
	}
	else if (!response || response.Status.code != 200) {
		$("#issueaddress").html(
				"Status Code:" + response.Status.code );
		return 'aaa';
	} else {
		place = response.Placemark[0];
		point = new GLatLng(place.Point.coordinates[1],place.Point.coordinates[0]);
		marker = new GMarker(point);
		
		$("#issueaddress").html(
				'<b>orig latlng:</b>' + place.Point.coordinates[1] + ", "+ place.Point.coordinates[0] + '<br/>' + 
				'<b>Address:</b>' + place.address + '<br>' 
				);
		
		var postalAddress = place.address.split(',')[1].replace(/^\s+|\s+$/g, '') ;

		$("#id_issuepostal").val( place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.PostalCode.PostalCodeNumber ) ;
		$("#id_issuecity").val(   place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName) ;

		$("#id_issuecountry").val(   place.AddressDetails.Country.CountryName) ;

		$("#id_issuelat").val( place.Point.coordinates[1] ); 
		$("#id_issuelng").val( place.Point.coordinates[0] );
	
		 return point;
	}
}


function zoomToCluster(nelng, nelat, swlng, swlat) {
	if( map.getExtInfoWindow() != null ){
		map.closeExtInfoWindow();
	}
	var bounds = new GLatLngBounds();
	bounds.extend(new GLatLng( nelat, nelng ));
	bounds.extend(new GLatLng( swlat, swlng ));
	map.setZoom(map.getBoundsZoomLevel(bounds)-1);
	map.setCenter(bounds.getCenter());
	
}

