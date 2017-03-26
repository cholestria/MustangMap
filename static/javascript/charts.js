//sets global value of 2016 as most recent year
var most_recent_year = 2016;

//shows the registration information on login page
function showRegistrationDiv(evt) {
    document.getElementById('registrationDiv').style.display = "block";
}

//allows for earch of the herd names on the herd search page
function searchHerds() {
    var input = document.getElementById('myInput');
    var filter = input.value.toUpperCase();
    var group = document.getElementById("list-group");
    var anchor_list = group.getElementsByTagName("a");

    // Loop through all list items, and hide those who don't match the search query
    for (var i = 0; i < anchor_list.length; i++) {
        var a = anchor_list[i];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            anchor_list[i].style.display = "";
        } else {
            anchor_list[i].style.display = "none";
        }
    }
}

//finds the center of a geojson feature
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

//loads initial map page with nationwide data
// function pageLoad() {
//     makePopulationChart("/totaldata", 'info-box');
//     makeAdoptionChart("/totaldata", 'info-box-2');
//     loadNationalTextInfoBox("/totaldata", 'text-info-box');
// }

//loads Heat Map
function displayHeatMap() {
    loadNationalFeatures();
    map.panTo({lat: 40, lng: -115});
    colorMap(2016);
}

//used in heatmap feature
function colorMap(year) {
  $.get("/popbyyear", function(popdata) {
      var that_year = popdata[year];
      var large_population = 10000;
      var medium_population = 5000;
      var small_population = 2000;
      map.data.forEach(function(feature) {
          var state_id = feature.getProperty('STATEID');
          var population_data = that_year[state_id];
          var horse_pop = population_data["horse"];
          var burro_pop = population_data["burro"];
          var sum_pop = horse_pop + burro_pop;
          if (sum_pop > large_population) {
            map.data.overrideStyle(feature, {fillColor: 'red'});
          } else if (sum_pop > medium_population) {
            map.data.overrideStyle(feature, {fillColor: 'orange'});
          } else if (sum_pop > small_population) {
            map.data.overrideStyle(feature, {fillColor: 'yellow'});
          } else {
            map.data.overrideStyle(feature, {fillColor: 'green'});
          }
      });
  });
}

//adds a thousands seperator into the text information
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

//creates a paragraph with national information to be used in the text information div
function loadNationalTextInfoBox(data, div_id) {
    var horses_population = numberWithCommas(data.PopData[most_recent_year][0]);
    var burros_population = numberWithCommas(data.PopData[most_recent_year][1]);
    var blm_acreage = numberWithCommas(data.PopData[most_recent_year][2]);
    var total_acreage = numberWithCommas(data.PopData[most_recent_year][3]);

    document.getElementById("text-head").innerHTML = "Mustang Map";

    var paragraph = "As of " + most_recent_year + " there were approximately " +
    "67,000 Mustangs and burros living in wild. The Bureau of Land Management " +
    "estimates - controversially - that there should only be 27,000. Every " +
    "year Mustangs are rounded up and placed in holding pens. Some are adopted " +
    "(sold) but most remain in holding for the rest of their lives. You can click " +
    "on the map or one of the buttons below to view population, removals, and " +
    "adoption information for that state.";
    document.getElementById("text-paragraph").innerHTML = paragraph;
}

//creates a paragraph with information about a state or herd in the text info box
function makeTextInfoBox(data, div_id) {
    var name = data.Name;
    var raw_horse_population = data.PopData[most_recent_year][0];
    var raw_burro_population = data.PopData[most_recent_year][1];
    var horse_population = numberWithCommas(raw_horse_population);
    var burro_population = numberWithCommas(data.PopData[most_recent_year][1]);
    var blm_acreage = numberWithCommas(data.PopData[most_recent_year][2]);
    var total_acreage = numberWithCommas(data.PopData[most_recent_year][3]);
    var pop_sentence;


    if (raw_horse_population === 0 && raw_burro_population === 0) {
        pop_sentence = "no Mustangs or burros";
    } else if (raw_horse_population === 0 && raw_burro_population > 0) {
        pop_sentence = "no Mustangs and " + burro_population + " burros";
    } else if (raw_horse_population > 0 && raw_burro_population === 0) {
        pop_sentence = horse_population + " Mustangs and no burros";
    } else {
        pop_sentence = horse_population + " Mustangs and " + burro_population + " burros";
    }
    document.getElementById("link-text").style.display = "block";

    document.getElementById("text-head").innerHTML = name;

    var paragraph = "As of " + most_recent_year + ", " + name + " had " +
      pop_sentence + " in the wild. The total acreage for this area is " +
      total_acreage + " acres." ;

    document.getElementById("text-paragraph").innerHTML = paragraph;
}

//alerts user to ability to click on herds and offers return to national data link
function makeHerdLink(div_id) {
    document.getElementById("link-text").style.display = "block";

    document.getElementById("link-text").innerHTML = "To view information about " +
    "each herd area, click on the herd area in the map.<br><br><br>" +
    "<a class='btn' id='state-link'>Click here</a> to return to the national map.";

    document.getElementById("state-link").onclick = function(event) {
    loadNationalFeatures();
    };
}

//displays a picture in the text info div when there is a picture available for that herd
function makeHerdPictureBox(data, div_id) {
    var picture_object = data.Pictures;
    var filename = Object.keys(picture_object);
    if (filename == "none") {
        document.getElementById("image-div").style.display = "none";
    } else {
    document.getElementById("link-text").style.display = "none";
    document.getElementById("image-div").style.display = "block";
    document.getElementById("image").src = "pictures/"+filename;
    }
}

//creates a link in the text info div to view that state's map
function makeStateLink(data, div_id) {
    var state_name = data.Name;
    var state_id = data.MapDict.state_id;
    var latitude = data.MapDict.latitude;
    var longitude = data.MapDict.longitude;
    var zoom = data.MapDict.zoom;
    var map_names = data.MapDict.map_names;

    if (state_name == 'California' || state_name == 'Idaho' || state_name == 'Montana' ||
     state_name == 'Utah' || state_name == 'Wyoming' || state_name == 'New Mexico') {
        document.getElementById("link-text").innerHTML = "Individual herd area " +
        "maps are not yet available for " + state_name + " Please check back later.";
    } else {
    document.getElementById("link-text").innerHTML =
    "<a class='btn' id='state-link'>Click here</a> to see a map of all of the" +
    " herd areas in " + state_name + ".";

    document.getElementById("state-link").onclick = function(event) {
        loadStateFeatures(state_id, map_names, {"lat": latitude, "lng": longitude}, zoom);
    };
    }
}

//passes json information into the highcharts chart to make the population chart
function makePopulationChart(data, div_id) {

    var name = data.Name; //state or herd name
    var horses_population = [];
    var burros_population = [];
    var blm_acreage = [];
    var other_acreage = [];

    var year_object=data.PopData;
    var years=Object.keys(year_object);

    for (var i=0; i < years.length; i++) {
        var year = years[i];
        horses_population.push(year_object[year][0]);
        burros_population.push(year_object[year][1]);
        blm_acreage.push(year_object[year][2]);
        other_acreage.push(year_object[year][3]);
    }

    if (name === "Nationwide") {
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
        legend: {
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

//passes information from a json into highcharts to make the adoptions chart
function makeAdoptionChart(data, div_id) {

    var header;
    var horses_adopted = [];
    var burros_adopted = [];
    var horses_removed = [];
    var burros_removed = [];

    var area_name=data.Name;
    var year_object=data.AdoptData;
    var years=Object.keys(year_object);
    var footnote_object=data.Footnotes;
    var footnote_list=Object.keys(footnote_object);
    var population_object=data.PopData;
    var pop_years=Object.keys(population_object);

    for (var i=0; i < years.length; i++) {
        var year = years[i];
        horses_adopted.push(year_object[year][0]);
        burros_adopted.push(year_object[year][1]);
        horses_removed.push(year_object[year][2]);
        burros_removed.push(year_object[year][3]);
    }

    if (area_name === "Nationwide") {
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
        legend: {
            itemStyle: {
            fontSize: 'small',
            },
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
            href: '/about',
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