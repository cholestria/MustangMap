function nameToId(name) {
  var name_dict = {'Arizona': 'AZ', 'California': 'CA', 'Colorado': 'CO', 'Eastern States': 'ES', 'Idaho': 'ID', 'Montana': 'MT', 'National Program': 'NAT', 'New Mexico': 'NM', 'Nevada': 'NV', 'Oregon': 'OR', 'Utah': 'UT', 'Wyoming': 'WY'};
  return name_dict[name];
}

function showRegistrationDiv(evt) {
    document.getElementById('registrationDiv').style.display = "block";
}

function searchHerds() {
    // Declare variables
    var input, filter, group, anchor_list, a, i;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    group = document.getElementById("list-group");
    anchor_list = group.getElementsByTagName("a");


    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < anchor_list.length; i++) {
        a = anchor_list[i];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            anchor_list[i].style.display = "";
        } else {
            anchor_list[i].style.display = "none";
        }
    }
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
    makeNationalTextInfoBox("/totaldata", 'text-info-box');
}

function nationalInfo() {
    makePopulationChart("/totaldata", 'info-box');
    makeAdoptionChart("/totaldata", 'info-box-2');
    makeNationalTextInfoBox("/totaldata", 'text-info-box');
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

function makeNationalTextInfoBox(popdata, div_id) {
    var most_recent_year = 2016;
    // var name = popdata.Name;
    var horses_population = popdata.PopData[most_recent_year][0];
    var burros_population = popdata.PopData[most_recent_year][1];
    var blm_acreage = popdata.PopData[most_recent_year][2];
    var total_acreage = popdata.PopData[most_recent_year][3];
    var header = document.getElementById("text-head");
    header.innerHTML = "Mustang Map";
    var paragraph_div = document.getElementById("text-paragraph");
    var paragraph = "As of " + most_recent_year + " there are approximately 67,000 Mustangs and burros living in wild. The Bureau of Land Management estimates - controversially - that there should only be 27,000. Every year Mustangs are rounded up and placed in holding pens. Some are adopted out, but most remain in holding for the rest of their lives. You can click on the map or one of the buttons below to view population, removals, and adoption information for that state.";
    paragraph_div.innerHTML = paragraph;
}

function makeTextInfoBox(popdata, div_id) {
    var most_recent_year = 2016;
    var name = popdata.Name;
    var horses_population = popdata.PopData[most_recent_year][0];
    var burros_population = popdata.PopData[most_recent_year][1];
    var blm_acreage = popdata.PopData[most_recent_year][2];
    var total_acreage = popdata.PopData[most_recent_year][3];

    var header = document.getElementById("text-head");
    header.innerHTML = name;

    var paragraph_div = document.getElementById("text-paragraph");
    var paragraph = "As of " + most_recent_year + ", " + name + " had " + horses_population + " Mustangs and " + burros_population + " burros in the wild. They are spread over " + total_acreage + " acres, " + blm_acreage + " of which are Bureau of Land Management acres. Non BLM acreage may be private land or managed by other ofices.";
    paragraph_div.innerHTML = paragraph;

    var state_id = popdata.MapDict.state_id;
    var latitude = popdata.MapDict.latitude;
    var longitude = popdata.MapDict.longitude;
    var zoom = popdata.MapDict.zoom;
    var map_names = popdata.MapDict.map_names;

    //document.getElementById("state-link").innerHTML = "Click Here";

    document.getElementById("link-text").innerHTML = "To see a map of all of the herd areas in this state <a class='btn' id='state-link'>click here.</a>";

    document.getElementById("state-link").onclick = function(event) {
        loadStateFeatures(state_id, map_names, {"lat": latitude, "lng": longitude}, zoom);
    };
}
// document.getElementById('buttonLED'+id).setAttribute('onclick','writeLED(1,1)')
// <a class="btn btn-sm btn-success" role="button" onclick="loadStateFeatures('{{state.state_id}}', ['{{ ("', '".join(state.file_names))|safe }}'], {lat: {{state.latitude}}, lng: {{state.longitude}} }, {{state.zoom}})">{{state.name}}</a>

function makePopulationChart(popdata, div_id) {

    var years = [];
    var year_object;
    var result = popdata;
    var name = result.Name; //state or herd name
    var horses_population = [];
    var burros_population = [];
    var blm_acreage = [];
    var other_acreage = [];

    // result=popdata;
    // name=result.Name;
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
}

function makeAdoptionChart(popdata, div_id) {

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

    result=popdata;
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
}