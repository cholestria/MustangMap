var clickHandler = function(event) {};

//initializes google mapps api with settings
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 40, lng: -115},
    draggable: false,
    scrollwheel: false,
    zoomControl: false,
    streetViewControl: false,
    styles: [{"featureType":"all","elementType":"all",
      "stylers":[{"hue":"#ffaa00"},{"saturation":"-33"},{"lightness":"10"}]},
      {"featureType":"administrative.locality","elementType":"labels.text.fill",
      "stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural.terrain",
      "elementType":"geometry","stylers":[{"visibility":"simplified"}]},
      {"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},
      {"featureType":"poi.attraction","elementType":"all",
      "stylers":[{"visibility":"off"}]},{"featureType":"poi.business",
      "elementType":"labels","stylers":[{"visibility":"off"}]},
      {"featureType":"poi.government","elementType":"all",
      "stylers":[{"visibility":"off"}]},{"featureType":"poi.place_of_worship",
      "elementType":"all","stylers":[{"visibility":"off"}]},
      {"featureType":"road.highway","elementType":"geometry",
      "stylers":[{"visibility":"simplified"}]},{"featureType":"road.highway",
      "elementType":"labels.text","stylers":[{"visibility":"on"}]},
      {"featureType":"road.arterial","elementType":"geometry",
      "stylers":[{"visibility":"simplified"}]},{"featureType":"transit.line",
      "elementType":"all","stylers":[{"visibility":"off"}]},
      {"featureType":"water","elementType":"geometry.fill",
      "stylers":[{"saturation":"-23"},{"gamma":"2.01"},{"color":"#f2f6f6"}]},
      {"featureType":"water","elementType":"geometry.stroke",
      "stylers":[{"saturation":"-14"}]}]
  });

  // Set the stroke width, and fill color for each polygon
  map.data.setStyle({
    fillColor: 'blue',
    strokeWeight: 1
  });

  // Set the fill color to purple when the feature is clicked.
  map.data.addListener('click', function(event) {
    map.data.overrideStyle(event.feature, {fillColor: 'purple'});
    // map.setZoom(5);
    var center = getCenter(event.feature);
    map.panTo(center);
  });


  // When the user hovers, tempt them to click by outlining the letters.
  // Call revertStyle() to remove all overrides. This will use the style rules
  // defined in the function passed to setStyle()
  map.data.addListener('mouseover', function(event) {
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, {strokeWeight: 3});
  });

  map.data.addListener('mouseout', function(event) {
    // map.data.revertStyle();
    map.data.overrideStyle(event.feature, {strokeWeight: 1});
  });

  // Set click event for each state feature.
  map.data.addListener('click', function(event){
    clickHandler(event);
  });
}

//loads national information into the map, charts, and text
function loadNationalFeatures() {

  map.data.forEach( function(feature) {
    map.data.remove(feature);
  });

  map.setZoom(4);
  map.setCenter({lat: 40, lng: -115});

  map.data.loadGeoJson('static/states.json');

  $.get("/totaldata", function(popdata) {
    makePopulationChart(popdata, 'info-box');
    makeAdoptionChart(popdata, 'info-box-2');
    loadNationalTextInfoBox(popdata, 'text-info-box');
    document.getElementById("link-text").innerHTML = "";
    document.getElementById("image-div").style.display = "none";
  });

//when national data is loaded, clicking on a state loads state information
// into the charts and text div
  clickHandler = function(event) {
    var state_id = event.feature.getProperty('STATEID');
    $.get("/statedata/"+state_id, function(popdata) {
      makePopulationChart(popdata, 'info-box');
      makeAdoptionChart(popdata, 'info-box-2');
      makeTextInfoBox(popdata, 'text-info-box');
      makeStateLink(popdata, 'text-info-box');
      document.getElementById("image-div").style.display = "none";
    });
  };
}


//loads a state's map, charts, and text information
function loadStateFeatures(state_id, file_names, center, zoom) {

  map.data.forEach( function(feature) {
    map.data.remove(feature);
  });

  for (i=0; i < file_names.length; i++) {
      map.data.loadGeoJson(file_names[i]);
  }
  map.setZoom(zoom);
  map.setCenter(center);

  $.get("/statedata/"+state_id, function(popdata) {
      makePopulationChart(popdata, 'info-box');
      makeAdoptionChart(popdata, 'info-box-2');
      makeTextInfoBox(popdata, 'info-box-2');
      makeHerdLink('info-box-2');
      document.getElementById("image-div").style.display = "none";
  });

  //if viewing a state map, clicks on a herd area load herd info in charts
  clickHandler = function(event) {
    //most states have 2 maps - one for HA and one for HMA
    var herd_id = event.feature.getProperty('HA_NO');
    if (!herd_id) {
      herd_id = event.feature.getProperty('HMA_ID');
    }
    $.get("/hachartdata/"+herd_id, function(popdata) {
      makePopulationChart(popdata, 'info-box');
      makeTextInfoBox(popdata, 'text-info-box');
      makeHerdPictureBox(popdata, 'image-div');
      document.getElementById("link-text").innerHTML = "";
    });
  };
}

//loads a herd's charts, and text information with state map
function loadHerdFeatures(state_id, file_names, center, zoom, herd_id) {

  map.data.forEach( function(feature) {
    map.data.remove(feature);
  });

  for (i=0; i < file_names.length; i++) {
      map.data.loadGeoJson(file_names[i]);
  }
  map.setZoom(zoom);
  map.setCenter(center);

  $.get("/statedata/"+state_id, function(popdata) {
      makeAdoptionChart(popdata, 'info-box-2');
  });

  loadHerdCharts(herd_id);
}

//used in loadHerdFeatures
function loadHerdCharts(herd_id) {
  $.get("/hachartdata/"+herd_id, function(popdata) {
  makePopulationChart(popdata, 'info-box');
  makeTextInfoBox(popdata, 'text-info-box');
  makeHerdPictureBox(popdata, 'image-div');
  document.getElementById("link-text").innerHTML = "";
  });
}

//loads initial map and charts on page load
//if the map is being loaded from the herd search and url parameters exist
//loads that state and herd's info
function mapLoader() {
  initMap();
  var urlParams = new URLSearchParams(window.location.search);
  var state_id_from_url = urlParams.get('state');
  var herd_id_from_url = urlParams.get('herd');
  if (herd_id_from_url && state_id_from_url) {
    for (var i=0; i<state_info_dict.length; i++) {
      if (state_info_dict[i].state_id === state_id_from_url) {
        loadHerdFeatures(state_id_from_url, state_info_dict[i].file_names,
        {"lat": state_info_dict[i].latitude, "lng": state_info_dict[i].longitude},
        state_info_dict[i].zoom, herd_id_from_url);
      }
    }
  } else if (state_id_from_url) {
    for (var j=0; j<state_info_dict.length; j++) {
      if (state_info_dict[j].state_id === state_id_from_url) {
        loadStateFeatures(state_id_from_url, state_info_dict[j].file_names,
        {"lat": state_info_dict[j].latitude, "lng": state_info_dict[j].longitude},
        state_info_dict[j].zoom);
      }
    }
  } else {
    loadNationalFeatures();
  }
}

