
ui.root.clear();
var map = ui.Map();
ui.root.add(map);
map.setOptions('SATELLITE');

var panel = ui.Panel({style: {width: '400px'}})
ui.root.add(panel);


var order = 2
var popMin = 0
var popMax = 2000000

function refresh(){
      var stationsFcNew = ee.FeatureCollection(stations)
              .filter(ee.Filter.lte('order', order))
              .filter(ee.Filter.gte('population', popMin))
              .filter(ee.Filter.lte('population', popMax))
    var layer = ui.Map.Layer(stationsFcNew, {color:"ff0000"}, 'Stations');
    map.layers().set(1, layer)
}

var select1 = ui.Slider(
  0, 2000000, 0, 10000,
  function(value){ 
    popMin = value
    refresh()
  }, 'horizontal', false,
  {width:"70%"})
var row1 = ui.Panel({layout: ui.Panel.Layout.flow('horizontal')})
row1.add(ui.Label('pop min'))
row1.add(select1)
panel.add(row1)

var select2 = ui.Slider(
  0, 2000000, 2000000, 10000,
  function(value){ 
    popMax = value
    refresh()
  }, 'horizontal', false,
  {width:"70%"})
var row2 = ui.Panel({layout: ui.Panel.Layout.flow('horizontal')})
row2.add(ui.Label('pop max'))
row2.add(select2)
panel.add(row2)

var powerFc = ee.FeatureCollection(power)
              .filter(ee.Filter.lte('order', order))

var stationsFc = ee.FeatureCollection(stations)
              .filter(ee.Filter.lte('order', order))


map.addLayer(coastline, {color:"00ff00"}, 'Coastline', false);

map.addLayer(stationsFc, {color:"ff0000"}, 'Stations');
map.addLayer(powerFc, {color:"0000ff"}, 'Power');
map.addLayer(transport.filter(ee.Filter.lte('type', 'port')), {color:"ffffff"}, 'Port');
map.addLayer(transport.filter(ee.Filter.lte('type', 'rail')), {color:"ffff00"}, 'Rail');
map.addLayer(transport.filter(ee.Filter.lte('type', 'port')), {color:"ffffff"}, 'Port');


// Define the chart and print it to the console.
var chartA =
    ui.Chart.feature
        .histogram({features: stationsFc.filter(ee.Filter.neq('population', null)), property: 'population', minBucketWidth: 100000})
        .setOptions({
          title: 'Population served',
          hAxis: {
            title: 'Population',
            titleTextStyle: {italic: false, bold: true},
            viewWindow: {min: -10, max: 2000000},
          },
          vAxis: {
            title: 'Count',
            titleTextStyle: {italic: false, bold: true},
            viewWindow: {min: 0, max: 1000}, logScale: true
          },
          colors: ['1d6b99'],
          legend: {position: 'none'}
        });
panel.add(chartA);

var stationsFc2 = stationsFc.filter(ee.Filter.neq('population', null)).filter(ee.Filter.neq('flow_mgd', null))
var arrPopulations = stationsFc2.reduceColumns(ee.Reducer.toList(), ['population']).get('list')
var arrFlow = stationsFc2.reduceColumns(ee.Reducer.toList(), ['flow_lps']).get('list')

var chartB = ui.Chart.array.values({
                    array: arrPopulations, 
                    axis: 0, 
                    xLabels: arrFlow
                    })
                .setOptions({
                  title: 'Flow rate across population',
                  hAxis: {
                    title: 'Flow (LPS)',
                    // viewWindow: {min: -124.50, max: -122.8},
                    titleTextStyle: {italic: false, bold: true}, logScale: true
                  },
                  vAxis: {
                    title: 'Population',
                    titleTextStyle: {italic: false, bold: true}, logScale: true
                  },
                  colors: ['1d6b99'],
                  // lineSize: 5,
                  pointSize: 1,
                  legend: {position: 'none'}
                });
panel.add(chartB);

var onClick = function(coords) {
// Create a point geometry from the clicked coordinates.
var point = ee.Geometry.Point(coords.lon, coords.lat).buffer(1000);// Filter the feature collection based on the clicked location.
var mergeFc = stationsFc.merge(powerFc)
var filtered = mergeFc.filterBounds(point);// Retrieve the attribute information for the clicked feature.
var info = filtered.toList(1);// Log the attribute information to the console.
print(ee.Feature(info.get(0)).toDictionary());
};// Add the click callback to the map.
map.onClick(onClick);