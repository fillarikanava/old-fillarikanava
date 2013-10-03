
/**
 * hila-script.js
 *
 * Kirjasto kaikkeen hienoon hila-asiaan. Ei ole obfuskoitu tätä, ei ole.
 *
 * @author Joukkue HILA
 */




/**
 ======================================================
 *
 * 1. Funktiokirjasto GoogleMaps-APIn käsittelyyn.
 *
 */


var map;
var geocoder;
var icon;
var this_issue_markers = [];
var mapW = 0;

var outerSW;
var outerNE;

var superStack = [];
var decorations = [];

var newMarker = null;

//bigMarkerStack has icon information as a tuple
//[0] marker
//[1] issue_data.options.icon.name
//[2] issue_data.options.icon.activeiconname
//[3] issue_data.options.icon.partlyactiveiconname])

var idStack = [];

var bigMarkerStack = new Object();
var idstack = new Object();



//These are for notifying user that new data is loaded from server.
//The first line has to be called in the template, to enable translations
//document.write('<div id="LoadingNewDataInfoDiv">Updating map data...</div>');



function issue_highlight(ids) {
	$.each(ids, function(count, place_id) {
		if ( idStack[place_id]  != null)
		{
			bigMarkerStack[ idStack[place_id] ][0].setImage(MEDIA_URL +  bigMarkerStack[ idStack[place_id] ][3]);
		}
	});
}


function stop_issue_highlight(ids) {
	$.each(ids, function(count, place_id) {
		if ( idStack[place_id]  != null)
		{
			bigMarkerStack[ idStack[place_id] ][0].setImage(MEDIA_URL +  bigMarkerStack[ idStack[place_id] ][1]);
		}
	});
}


function showIssue(issue_data, template, previewtemplate, clustertemplate)
{

	var icon = new GIcon();
	icon.image = MEDIA_URL + issue_data.options.icon.name;
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
		GEvent.addListener(marker, "mouseout", function()

				{
			marker.setImage(MEDIA_URL +issue_data.options.icon.name);
				});

		bigMarkerStack["cluster"+issue_data.screen_id]= [marker, issue_data.options.icon.name, issue_data.options.icon.activeiconname, issue_data.options.icon.partlyactiveiconname];
		$.each(issue_data.options.places, function(count, place_id) {
			idStack[place_id] = "cluster"+issue_data.screen_id;
		});
	}
	else
	{
		var markerstack = new Array();

		if (issue_data.point) {

            if (typeof(idStack[issue_data.point.id]) == 'undefined') {

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
                        if ($('#tab_'+issue_data.options.id))
                            $('#tab_'+issue_data.options.id).css({'background-color':'#84DFC1'});
                        $.each(markerstack, function(count, the_marker) {
                            the_marker.setImage(MEDIA_URL + issue_data.options.icon.activeiconname);
                        });
                    });
                    GEvent.addListener(issuemarker, "mouseout", function() {
                        if ($('#tab_'+issue_data.options.id))
                            $('#tab_'+issue_data.options.id).css({'background-color':'#FFFFFF'});
                        $.each(markerstack, function(count, the_marker) {
                            the_marker.setImage(MEDIA_URL +issue_data.options.icon.name);
                        });
                    });

                    bigMarkerStack[issue_data.options.points[0].id] = [issuemarker, issue_data.options.icon.name, issue_data.options.icon.activeiconname, issue_data.options.icon.partlyactiveiconname];
                    idStack[issue_data.options.points[0].id] = issue_data.options.points[0].id;
                }

            }
		}
		if (issue_data.options.comments)
		{
			$.each(issue_data.options.comments, function(count, i) {
				if (i.point)
				{

					//if (idStack[i.point.id] == null)
                    if (typeof(idStack[i.point.id]) == 'undefined')
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
								if ($('#tab_'+issue_data.options.id))
									$('#tab_'+issue_data.options.id).css({'background-color':'#84DFC1'});
								$.each(markerstack, function(count, the_marker) {
									the_marker.setImage(MEDIA_URL + issue_data.options.icon.activeiconname);
								});
							});
							GEvent.addListener(marker, "mouseout", function() {
								if ($('#tab_'+issue_data.options.id))
									$('#tab_'+issue_data.options.id).css({'background-color':'#FFFFFF'});
								$.each(markerstack, function(count, the_marker) {
									the_marker.setImage(MEDIA_URL +issue_data.options.icon.name);
								});
							});
						}

						if (document.getElementById("GUseMapCB")) {
							document.verifyform.GUseMapCB.checked = true;
						}

						bigMarkerStack[i.point.id] = [marker, issue_data.options.icon.name, issue_data.options.icon.activeiconname, issue_data.options.icon.partlyactiveiconname];
						idStack[i.point.id] = i.point.id;

					}
				}

			});

		}

	}
}



var interruptLoading = 0;
var currentLoadedData = 0;
var latestRequest = 1;
var loading_now = false;
var loading_queue = 0;

var updatesRunning = 0;
var filterChange = false;

function loadNewEvents(json_url, template, previewtemplate, clustertemplate, data)
{

	var sw = map.getBounds().getSouthWest();
	var ne = map.getBounds().getNorthEast();

	var dx = ne.lng() - sw.lng();
	var dy = ne.lat() - sw.lat();

	var d = $.extend(data, {
		x1: sw.lng() - 0.5 * dx,
		y1: sw.lat() - 0.5 * dy,
		x2: ne.lng() + 0.5 * dx,
		y2: ne.lat() + 0.5 * dy,
		zoomlevel: map.getZoom(),
		vlimit: 2000,
        slimit: 2000
	});


	zoomChange = false;
	if ( 2*dx < 0.9 * mapW || 2*dx > 1.1 *mapW )
	{ zoomChange = true; }

	if ( outerSW && outerNE &&
			ne.lng() < outerNE.lng() && ne.lat() < outerNE.lat() &&
			sw.lng() > outerSW.lng() && sw.lat() > outerSW.lat() && !zoomChange
            && !filterChange)
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
		if ( updatesRunning  < 1 )
		{
            updatesRunning = 1;
			map.getContainer().appendChild(NewDataInfoDiv);
			startTicker();
		}
		//		outerBounds = new GLatLngBounds(new GLatLng(d.x1, d.y1), new GLatLng(d.x2, d.y2) )

		outerSW = new GLatLng(d.y1, d.x1);
		outerNE = new GLatLng(d.y2, d.x2 );

        $.extend(d, get_search_filters() );
        filterChange = false;

		mapW = d.x2 - d.x1;

        $.extend(d, {seqnum: ++latestRequest} );

		$.ajax({
			url : json_url,
			data: d,
			dataType: 'json',
			success: function(data)
			{

                if (data[0]["seqnum"] < latestRequest)
                {
                    return;
                }

                map.clearOverlays();

                if (newMarker != null)
                {
                    map.addOverlay(newMarker);
                }

                bigMarkerStack = new Object;
                idStack = new Object;

                if (decorations)
                {
                    $.each (decorations, function(i, decoration) {
                        map.addOverlay(decoration);
                        if (data[0]["seqnum"] < latestRequest) { return; }
                    });
                }

                if (this_issue_markers)
                {
                    $.each (this_issue_markers, function(i, issueMarker) {
                        map.addOverlay(issueMarker);
                        if (data[0]["seqnum"] < latestRequest) { return; }
                    });
                }
                if (data[1])
                {
                    $.each(data[1], function(i, issue_data) {
                        showIssue(issue_data, template, previewtemplate, clustertemplate);
                        if (data[0]["seqnum"] < latestRequest) { return; }
                    });
                }
                if (data[0]["seqnum"] < latestRequest) { return; }

                updatesRunning = 0;
                map.getContainer().removeChild(NewDataInfoDiv);
                stopTicker();

			},
			error: function()
			{
				map.getContainer().removeChild(NewDataInfoDiv);
				stopTicker();
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





function get_search_filters() {
   var filters = new Object;
   if ($("#searchFilters") == null)
   {
       return filters;
   }
   filters['typefilter'] = $('#typefilter').val();
   if  ($('#keywordfilter').val() != "" )
   {
       filters['keywords'] = $('#keywordfilter').val();
   }
    if  ($('#date_from_filter').val() != "01/01/2009" )
    {
        filters['datefrom'] = $('#date_from_filter').val();
    }
    if  ($('#date_to_filter').val() != new Date().asString() )
    {
        filters['dateto'] = $('#date_to_filter').val();
    }


    if  ($("input[name='tagfilter']:checked").val() != "none" )
    {
       if  ($("input[name='tagfilter']:checked").val() == "untagged" )
        {
            filters['no_tags'] = "1";
        }
        else
       {
          filters['tag'] = $("input[name='tagfilter']:checked").val();
       }
    }
   return filters;
}

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
			$("#issueaddress").html('<b>orig latlng:</b>' + response.name + '<br/>' +
					'<b>Address:</b>' + place.address + '<br>'
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

        if ( typeof place.AddressDetails.Country.SubAdministrativeArea != 'undefined') {
            $("#id_issuepostal").val( place.AddressDetails.Country.SubAdministrativeArea.Locality.DependentLocality.PostalCode.PostalCodeNumber ) ;
            $("#id_issuecity").val(   place.AddressDetails.Country.SubAdministrativeArea.Locality.LocalityName) ;

        }
        else if ( typeof place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.PostalCode != 'undefined') {

            $("#id_issuepostal").val( place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.PostalCode.PostalCodeNumber ) ;
            $("#id_issuecity").val(   place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName) ;

        }
        else if ( typeof place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.DependentLocality.PostalCode != 'undefined') {

            $("#id_issuepostal").val( place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.DependentLocality.PostalCode.PostalCodeNumber ) ;
            $("#id_issuecity").val(   place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName) ;

        }


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

var getDataInfoInterval;
var tickerCounter = 0;
var dots = ['','.','..','...','....'];

function startTicker() {

	getDataInfoInterval = window.setInterval(function (a,b) {
		$("#ticker").html(dots[ tickerCounter % 5]);
		tickerCounter += 1;
	},300);

}

function stopTicker() {
	clearInterval(getDataInfoInterval);
}


/*
======================================================
 */
/**
 * Old hila-google-button.js
 *
 * @author Joukkue HILA
 */





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



/*
======================================================
 */
/**
 * hila peer moderation functions
 *
 * Tools for voting and such.
 *
 * @author Joukkue HILA
 */
//<![CDATA[


comment_vote_json_source = "";
ratingUrl = "";
imageUrl = "";
allowed_to_vote = 0;

function prepareButtons ( rateUrl, voteUrl , mediaUrl, allowVote ) {
	ratingUrl = rateUrl;
	comment_vote_json_source = voteUrl;
	imageUrl = mediaUrl;
	allowed_to_Vote = allowVote;
}

function displayRatingData(requestUrl, voteUrl, allowVote) {

	$.ajax({
		url : requestUrl,
		dataType: 'json',
		success:  function(data) {
		$.each(data, function(i, issue_data) {
			if (issue_data.issue_score != 'F')
			{
				if (allowed_to_vote == 0) {
					buttonFor     (issue_data.issue_id, -1,  0 );
					buttonAgainst (issue_data.issue_id, -1,  0 );
				}
				else if (issue_data.votecast > 0) {
					buttonFor     (issue_data.issue_id, -1,  0 );
					buttonAgainst (issue_data.issue_id, -1,  1 );
				}
				else  if (issue_data.votecast < 0) {
					buttonFor     (issue_data.issue_id, -1,  1 );
					buttonAgainst (issue_data.issue_id, -1,  0 );
				}
				else  {
					buttonFor     (issue_data.issue_id, -1,  1 );
					buttonAgainst (issue_data.issue_id, -1,  1 );
				}

				$( '#comment_-1_votesFor').html( issue_data.issue_votesfor);
				$( '#comment_-1_votesAgainst').html( issue_data.issue_votesagainst);

//				$( '#issue_' + issue_data.issue_id +'_score').html( issue_data.issue_score );
			}
			else
			{
				if (allowed_to_vote == 0) {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  0 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  0 );
				}
				else if (issue_data.votecast > 0) {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  0 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  1 );
				}
				else  if (issue_data.votecast < 0) {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  1 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  0 );
				}
				else  {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  1 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  1 );
				}

				$( '#comment_' + issue_data.comment_id +'_votesFor').html( issue_data.votesfor);
				$( '#comment_' + issue_data.comment_id +'_votesAgainst').html( issue_data.votesagainst);
			}
		})}})}



function loadCommentScores (json_url, issue_id, voteUrl) {
	displayRatingData (json_url + '?issue_id=' + issue_id, voteUrl);
}

function voteComment ( json_url, issue_id, message_id, value, voteUrl ) {
	displayRatingData (json_url + '?issue_id=' + issue_id + '&message_id=' + message_id + '&score=' +value);
}


function buttonFor(issue_id, comment_id, activate) {
	if (activate == 1)
		$('#comment_' + comment_id +'_buttonFor').html('<a href="#"  onclick="voteComment(\'' + comment_vote_json_source + "', '" + issue_id + '\' , \'' +comment_id+ '\', \'1\' );"><img src="'+ imageUrl + 'images/thumb-up-active.png" alt="Up"></a>');
	else
		$('#comment_' + comment_id +'_buttonFor').html('<img src="'+ imageUrl + 'images/thumb-up-deactive.png" alt="Up">');
}

function buttonAgainst(issue_id, comment_id, activate) {
	if (activate == 1)
		$('#comment_' + comment_id +'_buttonAgainst').html('<a href="#"  onclick="voteComment(\'' + comment_vote_json_source + "', '" + issue_id + '\' , \'' +comment_id+ '\', \'-1\' );"><img src="'+ imageUrl + 'images/thumb-down-active.png" alt="Down"></a>');
	else
		$('#comment_' + comment_id +'_buttonAgainst').html('<img src="'+ imageUrl + 'images/thumb-down-deactive.png" alt="Down">');
}

//]]>






/* RT search stuff */

//<![CDATA[

var lastupdate = 0;
var lastdata = 0;
var lastoffset = 0;
var waiting_text_search = false;




function dotheajaxthing(json_url,  view_limit, offset)
{
		waiting_text_search = false;

        var curFilters = get_search_filters();

		if (!curFilters)
			return;


//		if (keywordstring == lastdata && offset == lastoffset) {
//			return;
//		}
//		lastdata = keywordstring;

		lastoffset = offset;
		lastupdate += 1;


        d = { vlimit: view_limit,
              offset: offset,
              seqnum: lastupdate,
              details: "yes"
        };

        $.extend(d, curFilters );

		$.ajax({
			url : (json_url),
            data: d,
			dataType: 'json',
			success: function(data) {

//					if (!data[0] || lastupdate != data[0].seqnum) {
				if (!data[0]) {
					return;
				}
                $("#matches").html("");
                $("#matches").append("<div id=\"search_counts\">");

                if (data[0]["total_matches"] > 0 && view_limit > 0 ) {
//                    $("#matches").append("Roughly " + data[0]["total_matches"] + " hits. <br>");

                    var i = 1;
                    while ( i+view_limit < data[0]["total_matches"])
                    {
                        if (offset+view_limit < i+1 || offset+view_limit > i+view_limit) {
                            $("#matches").append(' <a href="javascript:dotheajaxthing(\''+json_url+'\','+view_limit+','+ (i-1)+');">'+ i + "-" + (i+view_limit-1) +" </a> ");
                        }
                        else {
                            $("#matches").append('<b>'+i + "-" + (i+view_limit-1) + '</b>');
                        }
                        i+=view_limit;
                    }
                    if (i<data[0]["total_matches"])
                    {
                        if (offset+view_limit < i+1 || offset+view_limit > i+view_limit) {
                            $("#matches").append(' <a href="javascript:dotheajaxthing(\''+json_url+'\','+view_limit+','+ (i-1)+');">'+ i + "-" + (data[0]["total_matches"]) +" </a> ");
                        }
                        else {
                            $("#matches").append('<b>'+i + "-" + (data[0]["total_matches"]) + '</b>');
                        }

                        i+=view_limit;
                    }
                }
                $("#matches").append("</div>");
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

function loadNewMatches (json_url, view_limit, offset)
{
	if (waiting_text_search == true)
		return;
	else
	{
		waiting_text_search = true;
		setTimeout( function() {dotheajaxthing(json_url, view_limit, offset)}, 300 );
	}

}

//]]>