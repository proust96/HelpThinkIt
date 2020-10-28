import 'ol/ol.css';
import GeoJSON from 'ol/format/GeoJSON';
import Map from 'ol/Map';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import OSM from 'ol/source/OSM';
import TileLayer from 'ol/layer/Tile';
import View from 'ol/View';
import {fromLonLat} from 'ol/proj';
import {Fill, Stroke, Style, Text} from 'ol/style';

var color_scale = chroma.scale(['green', 'red']);

var pollutionColor = function (nb){
  return new Style({
    stroke: new Stroke({
      color: color_scale(nb/10).hex(),
      width: 1,
    }),
    fill: new Fill({
      color: color_scale(nb/10).hex()+"BB",
    }),
  })
}

var vectorLayer = new VectorLayer({
  source: new VectorSource({
    url: 'https://raw.githubusercontent.com/proust96/files/main/districts.json',
    format: new GeoJSON(),
  }),
  style: function(feature){
    return pollutionColor(feature.get('name'))
  }
});

var baseLayer = new TileLayer({
  source: new OSM(),
  style: new Style({
    fill:new Fill({
      color: 'rgba(255,0,0,0.5)',
    })
  })
});

var map = new Map({
  layers: [baseLayer, vectorLayer],
  target: 'map',
  view: new View({
    center: fromLonLat([24.937054, 60.199493]),
    zoom: 12
  }),
});

var highlightStyle = function(nb) { return new Style({
  stroke: new Stroke({
    color: color_scale(nb/10).hex(),
    width: 1,
  }),
  fill: new Fill({
    color: color_scale(nb/10).hex()+"BB",
  }),
  text: new Text({
    font: '12px Calibri,sans-serif',
    fill: new Fill({
      color: '#000',
    }),
    stroke: new Stroke({
      color: '#f00',
      width: 3,
    }),
  }),
})};

var featureOverlay = new VectorLayer({
  source: new VectorSource(),
  map: map,
  style: function(feature){
    return highlightStyle(feature.get('name'))
  }
});

var highlight;
var displayFeature = function (pixel) {
  var feature = map.forEachFeatureAtPixel(pixel, function (feature) {
    return feature;
  });
  if (feature) {
    map.getTargetElement().style.cursor="pointer";
  } else {
    map.getTargetElement().style.cursor="default";
  }

  if (feature !== highlight) {
    if (highlight) {
      featureOverlay.getSource().removeFeature(highlight);
    }
    if (feature) {
      featureOverlay.getSource().addFeature(feature);
    }
    highlight = feature;
  }
};
var clickFeature = function (pixel) {
  var feature = map.forEachFeatureAtPixel(pixel, function (feature) {
    return feature;
  });
  var $right = $("#right");
  var $district_name = $(".district_name");
  var $district_pollution = $(".pollution_nb");
  if (feature) {
    $district_name.text("Cluster " + feature.getId());
    $district_pollution.text(feature.get("name"));
    $right.css("background-color", color_scale(feature.get('name')/10).hex()+"BB");
    showRight();
  } else {
    $district_name.text("Cluster ");
    $district_pollution.text("");
    $right.css("background-color","#EEEEEE");
    hideRight();
  }
};

map.on('pointermove', function (evt) {
  if (evt.dragging) {
    return;
  }
  var pixel = map.getEventPixel(evt.originalEvent);
  displayFeature(pixel);
});

map.on('click', function (evt) {
  clickFeature(evt.pixel);
});

var hideRight = function(){
  $(".right_top").hide();
  $(".right_transp").hide();
  $(".right_vehicle_content_bloc.selected").removeClass("selected");
  $(".nothing").show();
}
var showRight = function(){
  $(".right_top").show();
  $(".right_transp").show();
  $(".right_vehicle_content_bloc.car").addClass("selected");
  $(".nothing").hide();
}

hideRight();

$(".right_vehicle_logo").click(function(){
  $(".right_vehicle_logo.selected").removeClass("selected");
  $(".right_vehicle_content_bloc.selected").removeClass("selected");
  var sel_class=$(this).attr("class").split(/\s+/)[1];
  console.log(sel_class);
  $(this).addClass("selected");
  $(".right_vehicle_content_bloc."+sel_class).addClass("selected");
});
