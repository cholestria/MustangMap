function nameToId(name) {
  var name_dict = {'Arizona': 'AZ', 'California': 'CA', 'Colorado': 'CO', 'Eastern States': 'ES', 'Idaho': 'ID', 'Montana': 'MT', 'National Program': 'NAT', 'New Mexico': 'NM', 'Nevada': 'NV', 'Oregon': 'OR', 'Utah': 'UT', 'Wyoming': 'WY'};
  return name_dict[name];
}

function getCenter(feature) {
  var bounds = new google.maps.LatLngBounds();
  var listOfLatLngs = [];
  var geometry = feature.getGeometry();
  geometry.forEachLatLng(function(latlng) {
    listOfLatLngs.push(latlng);
  });
  for (var j = 0; j < listOfLatLngs.length; j++) {
    bounds.extend(listOfLatLngs[j]);
  }
  return bounds.getCenter();
}

function pageLoad() {
    makePopulationChart("/totaldata", 'info-box');
    makeAdoptionChart("/totaldata", 'info-box-2');
}

function nationalInfo() {
    makePopulationChart("/totaldata", 'info-box');
    makeAdoptionChart("/totaldata", 'info-box-2');
    map.panTo({lat: 40, lng: -115});
    colorMap(2015);
}

function colorMap(year) {
var that_year = pop_data[year];
map.data.forEach(function(feature) {
  var state_id = nameToId(feature.getProperty('NAME'));
  var population_data = that_year[state_id];
  var horse_pop = population_data["horse"];
  var burro_pop = population_data["burro"];
  var sum_pop = horse_pop + burro_pop;
  if (sum_pop > 10000) {
    map.data.overrideStyle(feature, {fillColor: 'red'});
  } else if (sum_pop > 5000) {
    map.data.overrideStyle(feature, {fillColor: 'orange'});
  } else if (sum_pop > 2000) {
    map.data.overrideStyle(feature, {fillColor: 'yellow'});
  } else {
    map.data.overrideStyle(feature, {fillColor: 'green'});
  }
});
}

function makePopulationChart(data_endpoint, div_id) {
    // Make a AJAX call to get the json data for the state
    $.get(data_endpoint, function(popdata) {

        var years = [];
        var year_object;
        var result;
        var name; //state or herd name
        var horses_population = [];
        var burros_population = [];
        var blm_acreage = [];
        var other_acreage = [];

        result=popdata;
        name=result.Name;
        year_object=result.PopData;
        years=Object.keys(year_object);

        for (var i=0; i < years.length; i++) {
            var year = years[i];
            horses_population.push(year_object[year][0]);
            burros_population.push(year_object[year][1]);
            blm_acreage.push(year_object[year][2]);
            other_acreage.push(year_object[year][3]);
        }

        if (name == "Nationwide") {
            header = "Population and Acreage " + name + " Over Time";
        } else {
            header = "Population and Acreage in " + name + " Over Time";
        }

        Highcharts.setOptions({
            lang: {
                thousandsSep: ','
            }
        });

        Highcharts.chart(div_id, {
            chart: {
                zoomType: 'xy'
            },
            title: {
                text: header
            },
            subtitle: {
                text: "Source: BLM"
            },
            legend: {
                // layout: 'vertical',
                // align: 'left',
                // verticalAlign: 'top',
                // // x: 400,
                // y: 50,
                // floating: true,
                borderWidth: 0,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
            },
            xAxis: [{
                categories: years,
                crosshair: true
            }],
                yAxis: [{ // Primary yAxis
                labels: {
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Population',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }, { // Secondary yAxis
                title: {
                    text: 'Acreage',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                opposite: true
            }],
            tooltip: {
                shared: false
            },
            navigation: {
              buttonOptions: {
                enabled: false
              }
            },
            credits: {
              enabled: false
            },
            series: [{
                name: 'BLM Acres',
                type: 'column',
                yAxis: 1,
                data: blm_acreage,
                tooltip: {
                    valueSuffix: ' acres'
                }
            }, {
                name: 'Other Acres',
                type: 'column',
                yAxis: 1,
                data: other_acreage,
                tooltip: {
                    valueSuffix: ' acres'
                }
            }, {
                name: 'Horse Population',
                type: 'spline',
                data: horses_population,
                tooltip: {
                    valueSuffix: ' Horses'
                }
            }, {
                name: 'Burro Population',
                type: 'spline',
                data: burros_population,
                tooltip: {
                    valueSuffix: ' Burros'
                }

            }]
        });
    });
}

function makeAdoptionChart(data_endpoint, div_id) {
    // Make a AJAX call to get the json data for the state
    $.get(data_endpoint, function(data) {

        var years = [];
        var pop_years = [];
        var year_object;
        var footnote_object;
        var population_object;
        var footnote_list;
        var result;
        var header;
        var area_name;
        var horses_adopted = [];
        var burros_adopted = [];
        var horses_removed = [];
        var burros_removed = [];
        var horse_population = [];
        var burro_population = [];

        result=data;
        area_name=result.Name;
        year_object=result.StateData;
        years=Object.keys(year_object);
        footnote_object=result.Footnotes;
        footnote_list=Object.keys(footnote_object);
        population_object=result.PopData;
        pop_years=Object.keys(population_object);

        for (var i=0; i < years.length; i++) {
            var year = years[i];
            horses_adopted.push(year_object[year][0]);
            burros_adopted.push(year_object[year][1]);
            horses_removed.push(year_object[year][2]);
            burros_removed.push(year_object[year][3]);
        }

        if (area_name == "Nationwide") {
            header = "Adoptions and Removals " + area_name + " Over Time";
        } else {
            header = "Adoptions and Removals in " + area_name + " Over Time";
        }

        Highcharts.setOptions({
            lang: {
                thousandsSep: ','
            }
        });

        Highcharts.chart(div_id, {
            chart: {
                type: 'areaspline'
            },
            title: {
                text: header
            },
            subtitle: {
                text: "Source: BLM"
            },
            legend: {
                // layout: 'vertical',
                // align: 'left',
                // verticalAlign: 'top',
                // // x: 400,
                // y: 50,
                // floating: true,
                borderWidth: 0,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
            },
            xAxis: {
                categories: years,
            },
            yAxis: {
                title: {
                    text: '# of horses or burros'
                }
            },
            tooltip: {
                shared: false,
                valueSuffix: ' '
            },
            navigation: {
              buttonOptions: {
                enabled: false
              }
            },

            credits: {
                enabled: true,
                text: footnote_list,
                href: 'https://www.blm.gov/wo/st/en/prog/whbprogram/herd_management/Data.html',
                position: {
                    align: 'left',
                    x: 20
                }
            },
            plotOptions: {
                areaspline: {
                    fillOpacity: 0.5
                }
            },
            series: [{
                name: 'Horses Adopted',
                data: horses_adopted
            }, {
                name: 'Burros Adopted',
                data: burros_adopted
            }, {
                name: 'Horses Removed',
                data: horses_removed
            }, {
                name: 'Burros Removed',
                data: burros_removed
            }]
        });
     });
}