import json
import uuid
import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode # Import JsCode from commons.utils
import folium


DUMMY_DATA = {
        "set_view": {"coordinate": [37.8, -96], "zoom": 4},
        "type": "FeatureCollection",
        "totalFeatures": 4,
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "California",
                    "times": [
                        {"year": 2020, "value": 75, "description": "California data for 2020"},
                        {"year": 2021, "value": 82, "description": "California data for 2021"},
                        {"year": 2022, "value": 65, "description": "California data for 2022"},
                        {"year": 2023, "value": 90, "description": "California data for 2023"}
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-124.4, 32.5], [-124.4, 42.0], [-120.0, 42.0], 
                        [-120.0, 39.0], [-114.6, 35.0], [-114.6, 32.5], 
                        [-124.4, 32.5]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Between",
                    "times": [
                        {"year": 2020, "value": 70, "description": "Between data for 2020"},
                        {"year": 2021, "value": 75, "description": "Between data for 2021"},
                        {"year": 2022, "value": 85, "description": "Between data for 2022"},
                        {"year": 2023, "value": 55, "description": "Between data for 2023"},
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-114.6, 32.5],[-114.6, 36.5],[-106.6, 36.5],[-106.6, 31.8],[-114.6, 32.5],
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Texas",
                    "times": [
                        {"year": 2020, "value": 60, "description": "Texas data for 2020"},
                        {"year": 2021, "value": 55, "description": "Texas data for 2021"},
                        {"year": 2022, "value": 70, "description": "Texas data for 2022"},
                        {"year": 2023, "value": 65, "description": "Texas data for 2023"}
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-106.6, 31.8], [-106.6, 36.5], [-100.0, 36.5], 
                        [-100.0, 34.5], [-94.0, 34.5], [-94.0, 29.7], 
                        [-97.0, 26.0], [-106.6, 31.8]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "New York",
                    "times": [
                        {"year": 2020, "value": 85, "description": "New York data for 2020"},
                        {"year": 2021, "value": 78, "description": "New York data for 2021"},
                        {"year": 2022, "value": 90, "description": "New York data for 2022"},
                        {"year": 2023, "value": 88, "description": "New York data for 2023"}
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.7, 42.0], [-79.7, 45.0], [-73.3, 45.0], 
                        [-73.3, 40.5], [-74.7, 40.5], [-79.7, 42.0]
                    ]]
                }
            }
        ]
    }
# Create your views here.

def get_json_from_url(url):
    """
    Fetches JSON data from a URL and converts it to a Python dictionary.

    Args:
        url (str): The URL to fetch the JSON data from.

    Returns:
        dict: A Python dictionary representing the JSON data, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def read_json_to_dict(filepath):
    """
    Reads a JSON file and returns its content as a dictionary.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict: The JSON data as a dictionary, or None if an error occurs.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f: #adding encoding to handle different character sets.
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None
    except Exception as e: # Catch any other exceptions
        print(f"An unexpected error occurred: {e}")
        return None


# Data from url
def map_view(request):
    dummy_map_data = DUMMY_DATA

    data = get_json_from_url("https://geonode.themimu.info/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_polbnda_adm3_250k_mimu_1&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature")

    if data is None:
        data = dummy_map_data
    
    # Convert to JSON and ensure it's safe to use in templates
    context = {
        'map_data': json.dumps(data)
    }
    
    return render(request, "maplayers/mapPage.html", context)

def map_view2(request):
    dummy_map_data = DUMMY_DATA

    data = get_json_from_url("https://geonode.themimu.info/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_polbnda_adm3_250k_mimu_1&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature")

    if data is None:
        data = dummy_map_data
    
    data_html_code = '''
        <div id="side-panel">
            <h3 id="polygon-title">Polygon Info</h3>
            <p id="polygon-description">Click a polygon to see details.</p>
            <div id="mini-map"></div>
            <div id="region-data"></div>
        </div>
        <div id="main_map"></div>
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            const map = L.map('main_map',{
                zoomControl: false, // Removes the zoom control buttons (+/-)
                // scrollWheelZoom: false, // Disables zooming with the mouse wheel
                doubleClickZoom: false, // Disables zooming by double-clicking
                touchZoom: false, // Disables pinch-zoom on touch devices
                dragging: true // Keeps dragging enabled (set to false to disable panning)
            }).setView([20, 96.8], 6);
            
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
            
            const mapData = {json.dumps(data)};
            
            function getColor(value) {
                return value > 85 ? '#084594' :
                    value > 75 ? '#2171b5' :
                    value > 65 ? '#4292c6' :
                    value > 55 ? '#6baed6' :
                    value > 45 ? '#9ecae1' :
                    '#deebf7';
            }
            
            // function style(feature, year) {
            function style(feature) {
                // const timeInfo = feature.properties.times.find(t => t.year === year);
                // const value = timeInfo ? timeInfo.value : 0;
                return {
                    // fillColor: getColor(value),
                    fillColor: '#4292c6',
                    weight: 2,
                    opacity: 1,
                    color: 'white',
                    dashArray: '3',
                    fillOpacity: 0.7
                };
            }
            
            let currentYear = 2023;
            let currentLayers = [];

            let current_selected_layer = null;

            function updateMap() {
                currentLayers.forEach(layer => map.removeLayer(layer));
                currentLayers = [];

                mapData.features.forEach(feature => {
                    const layer = L.geoJSON(feature, {
                        style: () => style(feature), 
                        onEachFeature: (feature, layer) => {
                            // Show the popup on hover
                            layer.on("mouseover", function() {
                                // Show the popup on hover
                                layer.bindPopup(`<b>${feature.properties.ST}</b><br>Township Name: ${feature.properties.TS}<br>Township Name in Myanmar: ${feature.TS_MMR}`).openPopup();

                                // Highlight the polygon on hover
                                layer.setStyle({
                                    weight: 4,
                                    color: 'white',
                                    dashArray: '1',
                                });
                            });

                            // Reset style when mouse leaves
                            layer.on("mouseout", function() {
                                layer.closePopup();
                                layer.setStyle({
                                    weight: 2,
                                    color: 'white',
                                    dashArray: '3',
                                });
                                // layer.setStyle(style(feature)); // Resets to the original style
                            });

                            layer.on('click', (e) => {
                                handlePolygonClick(layer, feature)
                            });
                            // Calculate the centroid of the polygon
                            const center = layer.getBounds().getCenter();

                            // Create a number or text to display (for example, based on the feature index or value)
                            const numberLabel = feature.properties.OBJECTID;  // You can replace with any field like feature.ST or feature.properties.value

                            // Add the label as a marker with a custom div icon
                            const labelMarker = L.marker(center, {
                                icon: L.divIcon({
                                    className: 'polygon-number-label',  // Custom class for styling
                                    html: `<p style="color: black; font-size: 9px; font-weight: bold;">${numberLabel}</p>`,
                                    iconSize: [20, 20]  // Size of the number display
                                })
                            }).addTo(map);

                            // Add click event to the number label marker
                            labelMarker.on('click', function(e) {
                                handlePolygonClick(layer, feature);  // Trigger the same click functionality
                            });

                            // Set style when mouse over
                            labelMarker.on("mouseover", function() {
                                // Show the popup on hover
                                layer.bindPopup(`<b>${feature.properties.ST}</b><br>Township Name: ${feature.properties.TS}<br>Township Name in Myanmar: ${feature.TS_MMR}`).openPopup();

                                // Highlight the polygon on hover
                                layer.setStyle({
                                    weight: 4,
                                    color: 'white',
                                    dashArray: '1',
                                });
                            });

                            // Reset style when mouse leaves
                            labelMarker.on("mouseout", function() {
                                layer.closePopup();
                                layer.setStyle({
                                    weight: 2,
                                    color: 'white',
                                    dashArray: '3',
                                });
                                // layer.setStyle(style(feature)); // Resets to the original style
                            });
                        }
                    });
                    layer.addTo(map);
                    currentLayers.push(layer);
                });

                function handlePolygonClick(layer, feature) {
                    // Reset previous selected layer's style if any
                    if (current_selected_layer) {
                        current_selected_layer.setStyle({
                            fillColor: '#4292c6',  // Reset to original color
                            fillOpacity: 0.7
                        });
                    }

                    document.getElementById('polygon-title').innerHTML = `<h3>${feature.properties.TS} Township Info</h3>`;
                    document.getElementById('polygon-description').innerHTML = `<p>${feature.properties.ST}>${feature.properties.DT}>${feature.properties.TS}</p>`;
                    document.getElementById('info-panel').style.display = 'block';
                    document.getElementById('region-name').innerHTML = `<h4>${feature.properties.ST}</h4>`;
                    document.getElementById('region-data').innerHTML = `
                        <p>State Name: ${feature.properties.ST}</p>
                        <p>State Postcode: ${feature.properties.ST_PCODE}</p>
                        <p>DT Name: ${feature.properties.DT}</p>
                        <p>DT Postcode: ${feature.properties.DT_PCODE}</p>
                        <p>Township Name: ${feature.properties.TS}</p>
                        <p>Township Postcode: ${feature.properties.TS_PCODE}</p>
                        <p>Township Name in Myanmar: ${feature.properties.TS_MMR}</p>`;
                    layer.setStyle({
                        fillColor: 'red',
                        fillOpacity: 0.7
                    });
                    current_selected_layer = layer;

                    // Initialize or update mini-map
                    if (!window.miniMap) {
                        window.miniMap = L.map("mini-map", { 
                            zoomControl: false,
                            dragging: false,
                            doubleClickZoom: false,
                            scrollWheelZoom: false,
                            boxZoom: false,
                            keyboard: false,
                            attributionControl: false,
                            interactive: false // Disables interaction
                        }).setView(layer.getBounds().getCenter(), 5);
                        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(window.miniMap);
                    } else {
                        window.miniMap.setView(layer.getBounds().getCenter(), 8);
                        window.miniMap.eachLayer((l) => { if (l instanceof L.Polygon) window.miniMap.removeLayer(l); });
                    }

                    // Add the selected polygon to the mini-map
                    L.geoJSON(feature, { style: { color: "transparent", fillColor: "red", fillOpacity: 0.7 } }).addTo(window.miniMap);

                    // Fit the polygon within the mini-map
                    window.miniMap.fitBounds(layer.getBounds());
                }
            }
            
            const slider = document.getElementById('timeline-slider');
            noUiSlider.create(slider, {
                start: [2023],
                connect: true,
                step: 1,
                range: { 'min': 2020, 'max': 2023 },
                format: { to: value => Math.round(value), from: value => Math.round(value) }
            });
            
            slider.noUiSlider.on('update', function (values, handle) {
                currentYear = parseInt(values[handle]);
                updateMap();
            });
            
            updateMap();
        });
    </script>
        '''
    # Convert to JSON and ensure it's safe to use in templates
    context = {
        'map_data': json.dumps(data),
        'html_code': data_html_code
    }
    
    return render(request, "maplayers/mapPage2.html", context)


def map_view_jsonfile_data(request):
    dummy_map_data = {
        "set_view": {"coordinate": [37.8, -96], "zoom": 4},
        # "set_view": {"coordinate": [20, 96.8], "zoom": 5},
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-124.4, 32.5], [-124.4, 42.0], [-120.0, 42.0], 
                        [-120.0, 39.0], [-114.6, 35.0], [-114.6, 32.5], 
                        [-124.4, 32.5]
                    ]]
                },
                "ST": "California",
                "ST_PCODE": "Don't know",
                "DT": "Not available",
                "DT_PCODE": "Don't know",
                "TS": "Not available",
                "TS_PCODE": "Don't know",
                "TS_MMR": "Not available",
                "Pcode_V": "Not available",
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-114.6, 32.5],[-114.6, 36.5],[-106.6, 36.5],[-106.6, 31.8],[-114.6, 32.5],
                    ]]
                },
                "ST": "Between",
                "ST_PCODE": "Don't know",
                "DT": "Not available",
                "DT_PCODE": "Don't know",
                "TS": "Not available",
                "TS_PCODE": "Don't know",
                "TS_MMR": "Not available",
                "Pcode_V": "Not available",
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-106.6, 31.8], [-106.6, 36.5], [-100.0, 36.5], 
                        [-100.0, 34.5], [-94.0, 34.5], [-94.0, 29.7], 
                        [-97.0, 26.0], [-106.6, 31.8]
                    ]]
                },
                "ST": "Texas",
                "ST_PCODE": "Don't know",
                "DT": "Not available",
                "DT_PCODE": "Don't know",
                "TS": "Not available",
                "TS_PCODE": "Don't know",
                "TS_MMR": "Not available",
                "Pcode_V": "Not available",
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.7, 42.0], [-79.7, 45.0], [-73.3, 45.0], 
                        [-73.3, 40.5], [-74.7, 40.5], [-79.7, 42.0]
                    ]]
                },
                "ST": "New York",
                "ST_PCODE": "Don't know",
                "DT": "Not available",
                "DT_PCODE": "Don't know",
                "TS": "Not available",
                "TS_PCODE": "Don't know",
                "TS_MMR": "Not available",
                "Pcode_V": "Not available",
            }
        ]
    }
    
    map_data = read_json_to_dict("maplayers/csv2json_leaflet.json")

    if map_data is not None:
        data = {
            "set_view": {"coordinate": [20, 96.8], "zoom": 5},
            "features": map_data
        }
        # print(data)
    else:
        data = dummy_map_data
    
    # Convert to JSON and ensure it's safe to use in templates
    context = {
        'map_data': json.dumps(data)
    }
    
    return render(request, "maplayers/mapPage.html", context)


def map_view_with_timeline(request):
    time_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "California",
                    "times": [
                        {"year": 2020, "value": 75, "description": "California data for 2020"},
                        {"year": 2021, "value": 82, "description": "California data for 2021"},
                        {"year": 2022, "value": 65, "description": "California data for 2022"},
                        {"year": 2023, "value": 90, "description": "California data for 2023"}
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-124.4, 32.5], [-124.4, 42.0], [-120.0, 42.0], 
                        [-120.0, 39.0], [-114.6, 35.0], [-114.6, 32.5], 
                        [-124.4, 32.5]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Between",
                    "times": [
                        {"year": 2020, "value": 70, "description": "Between data for 2020"},
                        {"year": 2021, "value": 75, "description": "Between data for 2021"},
                        {"year": 2022, "value": 85, "description": "Between data for 2022"},
                        {"year": 2023, "value": 55, "description": "Between data for 2023"},
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-114.6, 32.5],[-114.6, 36.5],[-106.6, 36.5],[-106.6, 31.8],[-114.6, 32.5],
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Texas",
                    "times": [
                        {"year": 2020, "value": 60, "description": "Texas data for 2020"},
                        {"year": 2021, "value": 55, "description": "Texas data for 2021"},
                        {"year": 2022, "value": 70, "description": "Texas data for 2022"},
                        {"year": 2023, "value": 65, "description": "Texas data for 2023"}
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-106.6, 31.8], [-106.6, 36.5], [-100.0, 36.5], 
                        [-100.0, 34.5], [-94.0, 34.5], [-94.0, 29.7], 
                        [-97.0, 26.0], [-106.6, 31.8]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "New York",
                    "times": [
                        {"year": 2020, "value": 85, "description": "New York data for 2020"},
                        {"year": 2021, "value": 78, "description": "New York data for 2021"},
                        {"year": 2022, "value": 90, "description": "New York data for 2022"},
                        {"year": 2023, "value": 88, "description": "New York data for 2023"}
                    ]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.7, 42.0], [-79.7, 45.0], [-73.3, 45.0], 
                        [-73.3, 40.5], [-74.7, 40.5], [-79.7, 42.0]
                    ]]
                }
            }
        ]
    }

    # Convert to JSON and ensure it's safe to use in templates
    context = {
        'time_data': json.dumps(time_data)
    }
    
    return render(request, "maplayers/mapPage.html", context)


def org_struction_direct_html(request):
    return render(request, 'maplayers/orgStructureDHTML.html')


class MapClassView(TemplateView):
    template_name = "maplayers/mapPage2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dummy_map_data = DUMMY_DATA

        data = get_json_from_url("https://geonode.themimu.info/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_polbnda_adm3_250k_mimu_1&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature")

        if data is None:
            data = dummy_map_data

        # Initialize map centered on Myanmar
        myanmar_map = folium.Map(location=[21.9162, 95.9560], tiles="cartodb positron", zoom_start=6)

        # JavaScript function to handle click event and change region color
        click_js = """
        <script>
        function highlightFeature(e) {
            var layer = e.target;
            layer.setStyle({
                fillColor: 'red',
                fillOpacity: 0.7
            });
        }
        
        function resetHighlight(e) {
            var layer = e.target;
            layer.setStyle({
                fillColor: '#3182bd',
                fillOpacity: 0.6
            });
        }
        
        document.addEventListener("DOMContentLoaded", function() {
            var geoJsonLayers = document.querySelectorAll(".leaflet-interactive");
            geoJsonLayers.forEach(function(layer) {
                layer.addEventListener("click", highlightFeature);
                layer.addEventListener("mouseout", resetHighlight);
            });
        });
        </script>
        """

        # popup = folium.GeoJsonPopup(
        #     fields=["ST", "TS", "TS_MMR"],
        #     aliases=["State", "Township", "Township Name in Myanamr"],
        #     style="background-color: yellow;"
        # )

        # # Add GeoJSON layer
        # folium.GeoJson(
        #     data,
        #     name="Myanmar Townships",
        #     style_function=lambda feature: {
        #         "fillColor": "#3182bd",  # Default color
        #         "color": "white",
        #         "weight": 2,
        #         "fillOpacity": 0.6
        #     },
        #     highlight_function=lambda feature: {
        #         "weight": 4,
        #         "color": "yellow",
        #         "fillOpacity": 0.8
        #     },
        #     tooltip=folium.GeoJsonTooltip(fields=["TS", "ST"], aliases=["Township:", "State:"]),
        #     popup=popup
        # ).add_to(myanmar_map)

        # Create a feature group for each layer type
        feature_groups = {}
        
        # Process each feature in the GeoJSON
        for i, feature in enumerate(data.get('features', [])):
            # Extract properties for popup content
            properties = feature.get('properties', {})
            
            # Determine layer type
            layer_type = properties.get('type', 'default')
            
            # Create feature group if it doesn't exist
            if layer_type not in feature_groups:
                feature_groups[layer_type] = folium.FeatureGroup(name=layer_type)
            
            # Create popup content from properties
            popup_html = "<div style='width: 200px;'>"
            for key, value in properties.items():
                popup_html += f"<strong>{key}:</strong> {value}<br>"
            popup_html += "</div>"
            
            # Default color for this feature
            default_color = properties.get('color', '#3388ff')
            
            # Add the feature to the map with popup
            geo_json = folium.GeoJson(
                feature,
                name=properties.get('name', 'Unnamed'),
                style_function=lambda x, default_color=default_color: {
                    'fillColor': default_color,
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 0.7
                },
                highlight_function=lambda x: {
                    'weight': 3,
                    'fillOpacity': 0.8
                },
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=properties.get('name', 'Click for more info')
            )
            
            geo_json.add_to(feature_groups[layer_type])
        
        # Add each feature group to the map
        for group in feature_groups.values():
            group.add_to(myanmar_map)
        
        # Add layer control
        folium.LayerControl().add_to(myanmar_map)
        
        # Add JavaScript to handle click events and change colors
        click_script = """
        <script>
            // Store original colors and the currently selected feature
            var originalColors = {};
            var selectedFeature = null;
            var highlightColor = '#FF4500';
            
            // Function to wait for Leaflet to be fully loaded
            function waitForLeaflet(callback) {
                if (typeof L !== 'undefined') {
                    callback();
                } else {
                    setTimeout(function() { waitForLeaflet(callback); }, 100);
                }
            }
            
            // Main initialization function
            function initializeClickHandlers() {
                // Get all map containers
                var mapContainers = document.querySelectorAll('.folium-map');
                
                if (mapContainers.length === 0) {
                    // If map isn't ready yet, try again later
                    setTimeout(initializeClickHandlers, 500);
                    return;
                }
                
                // Get the first map container (there's usually only one)
                var mapContainer = mapContainers[0];
                
                // Get the Leaflet map instance
                // In Folium, the map is stored in the global window._leaflet_map variable
                var leafletMap = window._leaflet_map || window.leafletMap;
                
                if (!leafletMap) {
                    console.log("Searching for map instance...");
                    // Try to find the map by searching through global variables
                    for (var key in window) {
                        if (window[key] && 
                            typeof window[key] === 'object' && 
                            window[key] instanceof L.Map) {
                            leafletMap = window[key];
                            console.log("Found map instance:", key);
                            break;
                        }
                    }
                }
                
                if (!leafletMap) {
                    console.log("Map not ready yet, retrying...");
                    setTimeout(initializeClickHandlers, 500);
                    return;
                }
                
                console.log("Map instance found, setting up click handlers");
                
                // Function to reset previous selection
                function resetSelection() {
                    if (selectedFeature) {
                        var originalColor = originalColors[selectedFeature._leaflet_id];
                        if (originalColor) {
                            selectedFeature.setStyle({
                                fillColor: originalColor,
                                fillOpacity: 0.7
                            });
                        }
                        selectedFeature = null;
                    }
                }
                
                // Add click handlers to all GeoJSON layers
                leafletMap.eachLayer(function(layer) {
                    // Only process GeoJSON layers
                    if (layer.feature && layer.setStyle) {
                        // Store original color
                        var style = layer.options || {};
                        originalColors[layer._leaflet_id] = style.fillColor || '#3388ff';
                        
                        // Add click handler
                        layer.on('click', function(e) {
                            console.log("Layer clicked");
                            
                            // Reset previous selection
                            resetSelection();
                            
                            // Highlight this feature
                            selectedFeature = e.target;
                            e.target.setStyle({
                                fillColor: highlightColor,
                                fillOpacity: 0.9
                            });
                            
                            // Prevent click from propagating
                            if (e.originalEvent) {
                                L.DomEvent.stopPropagation(e.originalEvent);
                            }
                        });
                    }
                });
                
                // Reset selection when clicking map background
                leafletMap.on('click', function() {
                    console.log("Map clicked");
                    resetSelection();
                });
                
                console.log("Click handlers initialized");
            }
            
            // Wait for Leaflet and DOM to be ready
            document.addEventListener('DOMContentLoaded', function() {
                console.log("DOM loaded, waiting for Leaflet");
                waitForLeaflet(function() {
                    console.log("Leaflet loaded, initializing handlers");
                    // Give extra time for Folium to finish rendering
                    setTimeout(initializeClickHandlers, 1000);
                });
            });
        </script>
        """
        
        # Add custom CSS for hover effects
        custom_css = """
        <style>
            .leaflet-interactive {
                transition: fill 0.3s ease, stroke-width 0.3s ease;
            }
        </style>
        """
        
        # Add the script and CSS to the map
        myanmar_map.get_root().html.add_child(folium.Element(click_script))
        myanmar_map.get_root().html.add_child(folium.Element(custom_css))
        
        # Render to HTML string
        geo_html = myanmar_map._repr_html_()  # Render map as HTML

        context["html_code"] = geo_html

        return context