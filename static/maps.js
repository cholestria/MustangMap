var clickHandler = function(event) {};

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 40, lng: -115},
    draggable: false,
    scrollwheel: false,
    zoomControl: false,
    streetViewControl: false,
    styles: [{"featureType":"all","elementType":"all","stylers":[{"hue":"#ffaa00"},{"saturation":"-33"},{"lightness":"10"}]},{"featureType":"administrative.locality","elementType":"labels.text.fill","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural.terrain","elementType":"geometry","stylers":[{"visibility":"simplified"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.attraction","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.business","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"poi.government","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.place_of_worship","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"labels.text","stylers":[{"visibility":"on"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"visibility":"simplified"}]},{"featureType":"transit.line","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"saturation":"-23"},{"gamma":"2.01"},{"color":"#f2f6f6"}]},{"featureType":"water","elementType":"geometry.stroke","stylers":[{"saturation":"-14"}]}]

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
  loadNationalFeatures();
  // loadStateFeatures('OR', ['static/oregon_ha.geojson', 'static/oregon_hma.geojson'], {lat: 43.5, lng: -119.8}, 7);
}

function loadNationalFeatures() {

  map.data.forEach( function(feature) {
    map.data.remove(feature);
  });

  map.setZoom(4);
  map.setCenter({lat: 40, lng: -115});

  map.data.loadGeoJson('static/states.json');

  makePopulationChart("/totaldata", 'info-box');
  makeAdoptionChart("/totaldata", 'info-box-2');

  clickHandler = function(event) {
    var state_id = nameToId(event.feature.getProperty('NAME'));
    makePopulationChart("/statedata/"+state_id, 'info-box');
    makeAdoptionChart("/statedata/"+state_id, 'info-box-2');
  };
}

function loadStateFeatures(state_id, file_names, center, zoom) {

  map.data.forEach( function(feature) {
    map.data.remove(feature);
  });

  for (i=0; i < file_names.length; i++) {
      map.data.loadGeoJson(file_names[i]);
  }
  map.setZoom(zoom);
  map.setCenter(center);

  makePopulationChart("/statedata/"+state_id, 'info-box');
  makeAdoptionChart("/statedata/"+state_id, 'info-box-2');

  clickHandler = function(event) {
    var herd_id = event.feature.getProperty('HA_NO');
    if (!herd_id) {
      herd_id = event.feature.getProperty('HMA_ID');
    }
    makePopulationChart("/hachartdata/"+herd_id, 'info-box');
  };


}


