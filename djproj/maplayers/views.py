import json
import random
import uuid
from jinja2 import Template
import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode # Import JsCode from commons.utils
from folium import MacroElement, Map, GeoJson, Popup, LayerControl, Element, FeatureGroup
from pyecharts.charts import Line, Bar


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
        myanmar_map = Map(
            location=[20.6303, 96.5617], 
            tiles="cartodb positron", 
            zoom_start=5,
            zoom_control=False,
            scroll_wheel_zoom=False,
            touch_zoom=False,
            #position="absolute",
            width="100%",
            height=600,
        )
        # myanmar_map = Map()

        
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
                feature_groups[layer_type] = FeatureGroup(name=layer_type)
            
            # Create popup content from properties
            popup_html = "<div style='width: 200px;'>"
            for key, value in properties.items():
                popup_html += f"<strong>{key}:</strong> {value}<br>"
            popup_html += "</div>"
            
            # Default color for this feature
            default_color = properties.get('color', '#3388ff')
            
            # Add the feature to the map with popup
            geo_json = GeoJson(
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
                popup=Popup(popup_html, max_width=300),
                tooltip=properties.get('name', 'Click for more info')
            )
            
            geo_json.add_to(feature_groups[layer_type])
        
        # Add each feature group to the map
        for group in feature_groups.values():
            group.add_to(myanmar_map)
        
        # Add layer control
        LayerControl().add_to(myanmar_map)
        
        # Add JavaScript to handle click events and change colors
        click_script = """
        <script>
            // Store original colors and the currently selected feature
            var originalColors = {};
            var originalStyles = {};
            var selectedFeature = null;
            var highlightColor = '#FF4500';

            // Store original event handlers
            var originalHandlers = {};
            
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
                    //console.log("resetSelection click")
                    if (selectedFeature) {
                        //console.log("resetSelection click -", selectedFeature._leaflet_id);
                        var originalColor = originalColors[selectedFeature._leaflet_id];
                        var originalStyle = originalStyles[selectedFeature._leaflet_id];
                        if (originalColor) {
                            //console.log("originalColor -", originalColor);
                            //console.log("originalStyle.fillColor -", originalStyle.fillColor);
                            //selectedFeature.setStyle({
                            //    fillColor: originalColor,
                            //    fillOpacity: 0.7
                            //});
                            selectedFeature.setStyle(originalStyle);
                        }

                        // Restore the original event handlers if they exist
                        if (originalHandlers[selectedFeature._leaflet_id]) {
                            var handlers = originalHandlers[selectedFeature._leaflet_id];

                            // Re-enable mouseover hander if it existed
                            if (handlers.mouseover) {
                                selectedFeature.on('mouseover', handlers.mouseover);
                            }

                            // Re-enable mouseout handler if it existed
                            if (handlers.mouseout) {
                                selectedFeature.on('mouseout', handlers.mouseout);
                            }

                            // Clear stored handlers
                            delete originalHandlers[selectedFeature._leaflet_id];
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
                        originalStyles[layer._leaflet_id] = JSON.parse(JSON.stringify(style));

                        // Debug >>>>>
                        //console.log('style -', style);

                        // Add click handler
                        layer.on('click', function(e) {
                            console.log("Layer clicked");

                            // Debug >>>>>
                            console.log('Recorded (',e.target._leaflet_id,')', originalStyles[e.target._leaflet_id]);

                            // Debug >>>>>
                            //console.log('Before -', e.target.options);
                            
                            // Reset previous selection
                            resetSelection();
                            
                            // Highlight this feature
                            selectedFeature = e.target;
                            //console.log("click -", selectedFeature._leaflet_id);
                            //console.log("e.target -", e.target);
                            //console.log("e.target._events -", e.target._events);
                            
                            // Store original event handlers before removing them
                            originalHandlers[selectedFeature._leaflet_id] = {
                                mouseover: e.target._events && e.target._events.mouseover ?
                                            e.target._events.mouseover[0].fn : null,
                                mouseout: e.target._events && e.target._events.mouseout ?
                                            e.target._events.mouseout[0].fn : null
                            };

                            // Temporarily disable mouseover/mouseout for this layer only
                            e.target.off('mouseover');
                            e.target.off('mouseout');
                            
                            // Apply highlight style
                            e.target.setStyle({
                                fillColor: highlightColor,
                                fillOpacity: 0.9,
                                weight: 3
                            });

                            // Debug >>>>>
                            //console.log('After -', e.target.options);

                            // Bring to front (for overlapping polygons)
                            if (e.target.bringToFront) {
                                e.target.bringToFront();
                            }
                            
                            // Prevent click from propagating
                            if (e.originalEvent) {
                                L.DomEvent.stopPropagation(e.originalEvent);
                            }
                        });
                    }
                });
                
                // Reset selection when clicking map background
                leafletMap.on('click', function() {
                    //console.log("Map clicked");
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
            .folium-map {
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
            }
        </style>
        """
        
        # Add the script and CSS to the map
        myanmar_map.get_root().html.add_child(Element(click_script))
        myanmar_map.get_root().html.add_child(Element(custom_css))

        figure = myanmar_map.get_root()
        figure.width = "100%"
        figure.height = "600px"

        # file_object = open('folium_gen_html.html', 'w')
        # file_object.write(myanmar_map._repr_html_())
        # file_object.close(  )
        
        # Render to HTML string
        geo_html = myanmar_map._repr_html_()  # Render map as HTML

        context["html_code"] = geo_html

        return context
    


class MapClassView2(TemplateView):
    template_name = "maplayers/mapPage3.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dummy_map_data = DUMMY_DATA

        data = get_json_from_url("https://geonode.themimu.info/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_polbnda_adm3_250k_mimu_1&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature")

        if data is None:
            data = dummy_map_data

        # Initialize map centered on Myanmar
        myanmar_map = Map(
            location=[20.6303, 96.5617], 
            tiles="cartodb positron", 
            zoom_start=5,
            zoom_control=False,
            scroll_wheel_zoom=False,
            touch_zoom=False,
            #position="absolute",
            width="100%",
            height=600,
        )
        # myanmar_map = Map()

        
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
                feature_groups[layer_type] = FeatureGroup(name=layer_type)
            
            # Create popup content from properties
            popup_html = "<div style='width: 200px;'>"
            for key, value in properties.items():
                popup_html += f"<strong>{key}:</strong> {value}<br>"
            popup_html += "</div>"
            
            # Default color for this feature
            default_color = properties.get('color', '#3388ff')
            
            # Add the feature to the map with popup
            geo_json = GeoJson(
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
                popup=Popup(popup_html, max_width=300),
                tooltip=properties.get('name', 'Click for more info')
            )
            
            geo_json.add_to(feature_groups[layer_type])
        
        # Add each feature group to the map
        for group in feature_groups.values():
            group.add_to(myanmar_map)
        
        # Add layer control
        LayerControl().add_to(myanmar_map)
        
        # Add JavaScript to handle click events and change colors
        click_script = """
        <script>
            // Store original colors and the currently selected feature
            var originalColors = {};
            var originalStyles = {};
            var selectedFeature = null;
            var highlightColor = '#FF4500';

            // Store original event handlers
            var originalHandlers = {};
            
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
                    //console.log("resetSelection click")
                    if (selectedFeature) {
                        //console.log("resetSelection click -", selectedFeature._leaflet_id);
                        var originalColor = originalColors[selectedFeature._leaflet_id];
                        var originalStyle = originalStyles[selectedFeature._leaflet_id];
                        if (originalColor) {
                            //console.log("originalColor -", originalColor);
                            //console.log("originalStyle.fillColor -", originalStyle.fillColor);
                            //selectedFeature.setStyle({
                            //    fillColor: originalColor,
                            //    fillOpacity: 0.7
                            //});
                            selectedFeature.setStyle(originalStyle);
                        }

                        // Restore the original event handlers if they exist
                        if (originalHandlers[selectedFeature._leaflet_id]) {
                            var handlers = originalHandlers[selectedFeature._leaflet_id];

                            // Re-enable mouseover hander if it existed
                            if (handlers.mouseover) {
                                selectedFeature.on('mouseover', handlers.mouseover);
                            }

                            // Re-enable mouseout handler if it existed
                            if (handlers.mouseout) {
                                selectedFeature.on('mouseout', handlers.mouseout);
                            }

                            // Clear stored handlers
                            delete originalHandlers[selectedFeature._leaflet_id];
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
                        originalStyles[layer._leaflet_id] = JSON.parse(JSON.stringify(style));

                        // Debug >>>>>
                        //console.log('style -', style);

                        // Add click handler
                        layer.on('click', function(e) {
                            console.log("Layer clicked");

                            // Debug >>>>>
                            console.log('Recorded (',e.target._leaflet_id,')', originalStyles[e.target._leaflet_id]);

                            // Debug >>>>>
                            //console.log('Before -', e.target.options);
                            
                            // Reset previous selection
                            resetSelection();
                            
                            // Highlight this feature
                            selectedFeature = e.target;
                            //console.log("click -", selectedFeature._leaflet_id);
                            //console.log("e.target -", e.target);
                            //console.log("e.target._events -", e.target._events);
                            
                            // Store original event handlers before removing them
                            originalHandlers[selectedFeature._leaflet_id] = {
                                mouseover: e.target._events && e.target._events.mouseover ?
                                            e.target._events.mouseover[0].fn : null,
                                mouseout: e.target._events && e.target._events.mouseout ?
                                            e.target._events.mouseout[0].fn : null
                            };

                            // Temporarily disable mouseover/mouseout for this layer only
                            e.target.off('mouseover');
                            e.target.off('mouseout');
                            
                            // Apply highlight style
                            e.target.setStyle({
                                fillColor: highlightColor,
                                fillOpacity: 0.9,
                                weight: 3
                            });

                            // Debug >>>>>
                            //console.log('After -', e.target.options);

                            // Bring to front (for overlapping polygons)
                            if (e.target.bringToFront) {
                                e.target.bringToFront();
                            }
                            
                            // Prevent click from propagating
                            if (e.originalEvent) {
                                L.DomEvent.stopPropagation(e.originalEvent);
                            }
                        });
                    }
                });
                
                // Reset selection when clicking map background
                leafletMap.on('click', function() {
                    //console.log("Map clicked");
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
            .folium-map {
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
            }
        </style>
        """
        
        # Add the script and CSS to the map
        myanmar_map.get_root().html.add_child(Element(click_script))
        myanmar_map.get_root().html.add_child(Element(custom_css))

        figure = myanmar_map.get_root()
        figure.width = "100%"
        figure.height = "100%"
        
        # Render to HTML string
        geo_html = myanmar_map._repr_html_()  # Render map as HTML

        # ------------- PYECHARTS LINE CHART -------------
        line_chart = (
            Line(init_opts=opts.InitOpts(theme="light", width="100%", height="200px"))
            .add_xaxis(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
            .add_yaxis("Sales", [5, 20, 36, 10, 75, 90], is_smooth=True)
            .add_yaxis("Revenue", [15, 25, 40, 23, 55, 65], is_smooth=True)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Monthly Performance"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                legend_opts=opts.LegendOpts(pos_top="5%"),
            )
        )
        
        # ------------- PYECHARTS BAR CHART -------------
        bar_chart = (
            Bar(init_opts=opts.InitOpts(theme="light", width="100%", height="200px"))
            .add_xaxis(["Product A", "Product B", "Product C", "Product D"])
            .add_yaxis("Sales", [57, 134, 137, 129])
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Product Performance"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
            )
        )
        
        # Example data for text boxes
        metrics = {
            'total_sales': 1250,
            'growth': '+15%',
            'customers': 450,
            'satisfaction': '4.8/5'
        }

        # Generate the complete HTML for the dashboard using Bootstrap classes
        dashboard_html = f"""
        <!-- Dashboard Content using Bootstrap classes -->
        <div class="container-fluid">
            <!-- Top Row - Controls -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card bg-light">
                        <div class="card-body">
                            <h4 class="card-title">Dashboard Controls</h4>
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="dateRange">Date Range</label>
                                        <select class="form-control" id="dateRange">
                                            <option>Last 7 Days</option>
                                            <option>Last 30 Days</option>
                                            <option>Last 90 Days</option>
                                            <option>Custom Range</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="region">Region</label>
                                        <select class="form-control" id="region">
                                            <option>All Regions</option>
                                            <option>North America</option>
                                            <option>Europe</option>
                                            <option>Asia-Pacific</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="product">Product</label>
                                        <select class="form-control" id="product">
                                            <option>All Products</option>
                                            <option>Product A</option>
                                            <option>Product B</option>
                                            <option>Product C</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label>&nbsp;</label>
                                        <button class="btn btn-primary form-control">Apply Filters</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Bottom Row - Main Dashboard Content -->
            <div class="row">
                <!-- Left Column - Text Boxes -->
                <div class="col-md-3">
                    <div class="card h-100">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Key Metrics</h5>
                        </div>
                        <div class="card-body">
                            <div class="bg-light p-3 rounded mb-3 shadow-sm">
                                <div class="text-muted">Total Sales</div>
                                <div class="h4 mb-0">{metrics['total_sales']}</div>
                            </div>
                            <div class="bg-light p-3 rounded mb-3 shadow-sm">
                                <div class="text-muted">Growth Rate</div>
                                <div class="h4 mb-0">{metrics['growth']}</div>
                            </div>
                            <div class="bg-light p-3 rounded mb-3 shadow-sm">
                                <div class="text-muted">Active Customers</div>
                                <div class="h4 mb-0">{metrics['customers']}</div>
                            </div>
                            <div class="bg-light p-3 rounded mb-3 shadow-sm">
                                <div class="text-muted">Satisfaction Score</div>
                                <div class="h4 mb-0">{metrics['satisfaction']}</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Middle Column - Map -->
                <div class="col-md-5">
                    <div class="card h-100">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Geographic Distribution</h5>
                        </div>
                        <div class="card-body">
                            <div id="map-container" style="height:400px;">
                                {geo_html}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Right Column - Charts -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Performance Analytics</h5>
                        </div>
                        <div class="card-body">
                            <div style="height:200px;" class="mb-3">
                                {line_chart.render_embed()}
                            </div>
                            <div style="height:200px;">
                                {bar_chart.render_embed()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        """
        # print("line_chart -",line_chart.render_embed())
        # print("bar_chart -",bar_chart.render_embed())
        context["html_code"] = geo_html
        context["dashboard_html"] = dashboard_html

        # file_object = open('folium_gen_dashboard_html.html', 'w')
        # file_object.write(dashboard_html)
        # file_object.close(  )

        return context
    
class MapClassView3old(TemplateView):
    template_name = "maplayers/mapPage3.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create dummy data for regions that can be accessed when clicking on map features
        region_data = {
            'Region1': {
                'name': 'Yangon',
                'metrics': {
                    'total_sales': 450,
                    'growth': '+12%',
                    'customers': 180,
                    'satisfaction': '4.6/5'
                },
                'chart_data': {
                    'line': {
                        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        'sales': [15, 25, 36, 42, 55, 68],
                        'revenue': [25, 35, 45, 55, 65, 78]
                    },
                    'bar': {
                        'products': ['Product A', 'Product B', 'Product C', 'Product D'],
                        'sales': [45, 65, 80, 72]
                    }
                }
            },
            'Region2': {
                'name': 'Mandalay',
                'metrics': {
                    'total_sales': 380,
                    'growth': '+8%',
                    'customers': 150,
                    'satisfaction': '4.3/5'
                },
                'chart_data': {
                    'line': {
                        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        'sales': [10, 18, 25, 32, 45, 52],
                        'revenue': [20, 28, 38, 45, 48, 60]
                    },
                    'bar': {
                        'products': ['Product A', 'Product B', 'Product C', 'Product D'],
                        'sales': [35, 58, 72, 65]
                    }
                }
            },
            'Region3': {
                'name': 'Bago',
                'metrics': {
                    'total_sales': 290,
                    'growth': '+15%',
                    'customers': 120,
                    'satisfaction': '4.7/5'
                },
                'chart_data': {
                    'line': {
                        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        'sales': [8, 15, 22, 30, 42, 58],
                        'revenue': [12, 22, 33, 40, 55, 68]
                    },
                    'bar': {
                        'products': ['Product A', 'Product B', 'Product C', 'Product D'],
                        'sales': [28, 48, 62, 55]
                    }
                }
            },
            'default': {
                'name': 'All Regions',
                'metrics': {
                    'total_sales': 1250,
                    'growth': '+15%',
                    'customers': 450,
                    'satisfaction': '4.8/5'
                },
                'chart_data': {
                    'line': {
                        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        'sales': [25, 40, 60, 75, 95, 120],
                        'revenue': [40, 55, 70, 85, 100, 125]
                    },
                    'bar': {
                        'products': ['Product A', 'Product B', 'Product C', 'Product D'],
                        'sales': [85, 125, 155, 140]
                    }
                }
            }
        }

        # Convert region data to JSON for JavaScript access
        import json
        region_data_json = json.dumps(region_data)

        dummy_map_data = DUMMY_DATA

        data = get_json_from_url("https://geonode.themimu.info/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_polbnda_adm3_250k_mimu_1&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature")

        if data is None:
            data = dummy_map_data

        # Initialize map centered on Myanmar
        myanmar_map = Map(
            location=[20.6303, 96.5617], 
            tiles="cartodb positron", 
            zoom_start=5,
            zoom_control=False,
            scroll_wheel_zoom=True,
            touch_zoom=True,
            width="100%",
            height="100%",
        )
        
        # Create a feature group for each layer type
        feature_groups = {}
        
        # Process each feature in the GeoJSON
        for i, feature in enumerate(data.get('features', [])):
            # Extract properties for popup content
            properties = feature.get('properties', {})
            
            # Add region_id to properties for data linking
            properties['region_id'] = f"Region{i % 3 + 1}"  # Cycle through Region1, Region2, Region3
            
            # Determine layer type
            layer_type = properties.get('type', 'default')
            
            # Create feature group if it doesn't exist
            if layer_type not in feature_groups:
                feature_groups[layer_type] = FeatureGroup(name=layer_type)
            
            # Create popup content from properties
            popup_html = "<div style='width: 200px;'>"
            for key, value in properties.items():
                popup_html += f"<strong>{key}:</strong> {value}<br>"
            popup_html += "</div>"
            
            # Default color for this feature
            default_color = properties.get('color', '#3388ff')
            
            # Add the feature to the map with popup
            geo_json = GeoJson(
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
                popup=Popup(popup_html, max_width=300),
                tooltip=properties.get('name', 'Click for more info')
            )
            
            geo_json.add_to(feature_groups[layer_type])
        
        # Add each feature group to the map
        for group in feature_groups.values():
            group.add_to(myanmar_map)
        
        # Add layer control
        LayerControl().add_to(myanmar_map)
        
        # Add dashboard HTML to the map using a custom control
        dashboard_html = """
        <div id="dashboard-container" class="container-fluid p-2">
            <!-- Top Row - Controls -->
            <div class="row mb-3">
                <div class="col-12">
                    <div class="card bg-light">
                        <div class="card-body p-2">
                            <h5 class="card-title mb-2">Dashboard Controls</h5>
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="dateRange">Date Range</label>
                                        <select class="form-control form-control-sm" id="dateRange">
                                            <option>Last 7 Days</option>
                                            <option>Last 30 Days</option>
                                            <option>Last 90 Days</option>
                                            <option>Custom Range</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="region">Region</label>
                                        <select class="form-control form-control-sm" id="region">
                                            <option>All Regions</option>
                                            <option>North America</option>
                                            <option>Europe</option>
                                            <option>Asia-Pacific</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="product">Product</label>
                                        <select class="form-control form-control-sm" id="product">
                                            <option>All Products</option>
                                            <option>Product A</option>
                                            <option>Product B</option>
                                            <option>Product C</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label>&nbsp;</label>
                                        <button class="btn btn-primary btn-sm form-control">Apply Filters</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Bottom Row - Side Panels -->
            <div class="row">
                <!-- Left Column - Text Boxes -->
                <div class="col-md-3">
                    <div class="card h-100">
                        <div class="card-header py-2">
                            <h6 class="card-title mb-0" id="metrics-title">Key Metrics</h6>
                        </div>
                        <div class="card-body p-2">
                            <div class="bg-light p-2 rounded mb-2 shadow-sm">
                                <div class="text-muted small">Total Sales</div>
                                <div class="h5 mb-0" id="metric-total-sales">1250</div>
                            </div>
                            <div class="bg-light p-2 rounded mb-2 shadow-sm">
                                <div class="text-muted small">Growth Rate</div>
                                <div class="h5 mb-0" id="metric-growth">+15%</div>
                            </div>
                            <div class="bg-light p-2 rounded mb-2 shadow-sm">
                                <div class="text-muted small">Active Customers</div>
                                <div class="h5 mb-0" id="metric-customers">450</div>
                            </div>
                            <div class="bg-light p-2 rounded mb-2 shadow-sm">
                                <div class="text-muted small">Satisfaction Score</div>
                                <div class="h5 mb-0" id="metric-satisfaction">4.8/5</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Right Column - Charts -->
                <div class="col-md-3">
                    <div class="card h-100">
                        <div class="card-header py-2">
                            <h6 class="card-title mb-0" id="charts-title">Performance Analytics</h6>
                        </div>
                        <div class="card-body p-2">
                            <div style="height:150px;" class="mb-2">
                                <canvas id="line-chart"></canvas>
                            </div>
                            <div style="height:150px;">
                                <canvas id="bar-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Create custom control for the dashboard
        dashboard_control = MacroElement()
        dashboard_control._template = Template(
            """
            {% macro script(this, kwargs) %}
            var dashboardControl = L.control({position: 'topleft'});
            dashboardControl.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'dashboard-control');
                div.innerHTML = `{{ this.dashboard_html }}`;
                div.style.width = '500px';
                div.style.backgroundColor = 'white';
                div.style.padding = '10px';
                div.style.borderRadius = '5px';
                div.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
                
                // Prevent click events from propagating to the map
                L.DomEvent.disableClickPropagation(div);
                L.DomEvent.disableScrollPropagation(div);
                
                return div;
            };
            dashboardControl.addTo({{ this._parent.get_name() }});
            {% endmacro %}
            """
        )
        dashboard_control.dashboard_html = dashboard_html
        myanmar_map.add_child(dashboard_control)
        
        # Add chart.js library
        chart_js = Element(
            """
            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.1/chart.min.js"></script>
            """
        )
        myanmar_map.get_root().html.add_child(chart_js)
        
        # Add JavaScript to handle click events and update dashboard
        click_script = f"""
        <script>
            // Store the region data for access when clicking on regions
            var regionData = {region_data_json};
            
            // Store original colors and the currently selected feature
            var originalColors = {{}};
            var originalStyles = {{}};
            var selectedFeature = null;
            var highlightColor = '#FF4500';
            
            // Initialize charts
            var lineChart, barChart;
            
            // Store original event handlers
            var originalHandlers = {{}};
            
            // Function to wait for Leaflet to be fully loaded
            function waitForLeaflet(callback) {{
                if (typeof L !== 'undefined') {{
                    callback();
                }} else {{
                    setTimeout(function() {{ waitForLeaflet(callback); }}, 100);
                }}
            }}
            
            // Function to initialize the charts
            function initCharts() {{
                const lineCtx = document.getElementById('line-chart').getContext('2d');
                lineChart = new Chart(lineCtx, {{
                    type: 'line',
                    data: {{
                        labels: regionData.default.chart_data.line.months,
                        datasets: [
                            {{
                                label: 'Sales',
                                data: regionData.default.chart_data.line.sales,
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                tension: 0.4
                            }},
                            {{
                                label: 'Revenue',
                                data: regionData.default.chart_data.line.revenue,
                                borderColor: 'rgba(153, 102, 255, 1)',
                                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                tension: 0.4
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'top',
                                labels: {{
                                    boxWidth: 10,
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }},
                            x: {{
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
                
                const barCtx = document.getElementById('bar-chart').getContext('2d');
                barChart = new Chart(barCtx, {{
                    type: 'bar',
                    data: {{
                        labels: regionData.default.chart_data.bar.products,
                        datasets: [
                            {{
                                label: 'Sales',
                                data: regionData.default.chart_data.bar.sales,
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.6)',
                                    'rgba(54, 162, 235, 0.6)',
                                    'rgba(255, 206, 86, 0.6)',
                                    'rgba(75, 192, 192, 0.6)'
                                ],
                                borderColor: [
                                    'rgba(255, 99, 132, 1)',
                                    'rgba(54, 162, 235, 1)',
                                    'rgba(255, 206, 86, 1)',
                                    'rgba(75, 192, 192, 1)'
                                ],
                                borderWidth: 1
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'top',
                                labels: {{
                                    boxWidth: 10,
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }},
                            x: {{
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Function to update dashboard with region data
            function updateDashboard(regionId) {{
                // Default to 'default' if regionId not found
                const data = regionData[regionId] || regionData.default;
                
                // Update metrics
                document.getElementById('metrics-title').textContent = `Key Metrics: ${{data.name}}`;
                document.getElementById('metric-total-sales').textContent = data.metrics.total_sales;
                document.getElementById('metric-growth').textContent = data.metrics.growth;
                document.getElementById('metric-customers').textContent = data.metrics.customers;
                document.getElementById('metric-satisfaction').textContent = data.metrics.satisfaction;
                
                // Update charts title
                document.getElementById('charts-title').textContent = `Performance: ${{data.name}}`;
                
                // Update line chart
                lineChart.data.labels = data.chart_data.line.months;
                lineChart.data.datasets[0].data = data.chart_data.line.sales;
                lineChart.data.datasets[1].data = data.chart_data.line.revenue;
                lineChart.update();
                
                // Update bar chart
                barChart.data.labels = data.chart_data.bar.products;
                barChart.data.datasets[0].data = data.chart_data.bar.sales;
                barChart.update();
            }}
            
            // Main initialization function
            function initializeClickHandlers() {{
                // Get all map containers
                var mapContainers = document.querySelectorAll('.folium-map');
                
                if (mapContainers.length === 0) {{
                    // If map isn't ready yet, try again later
                    setTimeout(initializeClickHandlers, 500);
                    return;
                }}
                
                // Initialize charts
                initCharts();
                
                // Get the Leaflet map instance
                var leafletMap = window._leaflet_map || window.leafletMap;
                
                if (!leafletMap) {{
                    console.log("Searching for map instance...");
                    // Try to find the map by searching through global variables
                    for (var key in window) {{
                        if (window[key] && 
                            typeof window[key] === 'object' && 
                            window[key] instanceof L.Map) {{
                            leafletMap = window[key];
                            console.log("Found map instance:", key);
                            break;
                        }}
                    }}
                }}
                
                if (!leafletMap) {{
                    console.log("Map not ready yet, retrying...");
                    setTimeout(initializeClickHandlers, 500);
                    return;
                }}
                
                console.log("Map instance found, setting up click handlers");
                
                // Function to reset previous selection
                function resetSelection() {{
                    if (selectedFeature) {{
                        var originalStyle = originalStyles[selectedFeature._leaflet_id];
                        if (originalStyle) {{
                            selectedFeature.setStyle(originalStyle);
                        }}

                        // Restore the original event handlers if they exist
                        if (originalHandlers[selectedFeature._leaflet_id]) {{
                            var handlers = originalHandlers[selectedFeature._leaflet_id];

                            // Re-enable mouseover hander if it existed
                            if (handlers.mouseover) {{
                                selectedFeature.on('mouseover', handlers.mouseover);
                            }}

                            // Re-enable mouseout handler if it existed
                            if (handlers.mouseout) {{
                                selectedFeature.on('mouseout', handlers.mouseout);
                            }}

                            // Clear stored handlers
                            delete originalHandlers[selectedFeature._leaflet_id];
                        }}

                        selectedFeature = null;
                    }}
                    
                    // Reset dashboard to default when no region selected
                    updateDashboard('default');
                }}
                
                // Add click handlers to all GeoJSON layers
                leafletMap.eachLayer(function(layer) {{
                    // Only process GeoJSON layers
                    if (layer.feature && layer.setStyle) {{
                        // Store original style
                        var style = layer.options || {{}};
                        originalColors[layer._leaflet_id] = style.fillColor || '#3388ff';
                        originalStyles[layer._leaflet_id] = JSON.parse(JSON.stringify(style));

                        // Add click handler
                        layer.on('click', function(e) {{
                            console.log("Layer clicked");
                            
                            // Reset previous selection
                            resetSelection();
                            
                            // Highlight this feature
                            selectedFeature = e.target;
                            
                            // Store original event handlers before removing them
                            originalHandlers[selectedFeature._leaflet_id] = {{
                                mouseover: e.target._events && e.target._events.mouseover ?
                                            e.target._events.mouseover[0].fn : null,
                                mouseout: e.target._events && e.target._events.mouseout ?
                                            e.target._events.mouseout[0].fn : null
                            }};

                            // Temporarily disable mouseover/mouseout for this layer only
                            e.target.off('mouseover');
                            e.target.off('mouseout');
                            
                            // Apply highlight style
                            e.target.setStyle({{
                                fillColor: highlightColor,
                                fillOpacity: 0.9,
                                weight: 3
                            }});

                            // Bring to front (for overlapping polygons)
                            if (e.target.bringToFront) {{
                                e.target.bringToFront();
                            }}
                            
                            // Get region_id from feature properties
                            var properties = e.target.feature.properties;
                            var regionId = properties.region_id || 'default';
                            
                            // Update dashboard with region data
                            updateDashboard(regionId);
                            
                            // Prevent click from propagating
                            if (e.originalEvent) {{
                                L.DomEvent.stopPropagation(e.originalEvent);
                            }}
                        }});
                    }}
                }});
                
                // Reset selection when clicking map background
                leafletMap.on('click', function() {{
                    console.log("Map clicked");
                    resetSelection();
                }});
                
                console.log("Click handlers initialized");
            }}
            
            // Wait for Leaflet and DOM to be ready
            document.addEventListener('DOMContentLoaded', function() {{
                console.log("DOM loaded, waiting for Leaflet");
                waitForLeaflet(function() {{
                    console.log("Leaflet loaded, initializing handlers");
                    // Give extra time for Folium to finish rendering
                    setTimeout(initializeClickHandlers, 1000);
                }});
            }});
        </script>
        """

        # Add custom CSS for dashboard styling
        custom_css = """
        <style>
            .leaflet-interactive {
                transition: fill 0.3s ease, stroke-width 0.3s ease;
            }
            .folium-map {
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
            }
            /* Dashboard control position */
            .dashboard-control {
                position: absolute;
                top: 10px;
                left: 50px;
                z-index: 1000;
            }
            /* Make dashboard panels semi-transparent and less intrusive */
            #dashboard-container .card {
                background-color: rgba(255, 255, 255, 0.9);
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            /* Make charts more compact */
            .card-body {
                padding: 0.5rem;
            }
            /* Smaller text for dashboard */
            #dashboard-container {
                font-size: 0.85rem;
            }
            /* Make dashboard width responsive */
            @media (max-width: 768px) {
                .dashboard-control {
                    width: 90% !important;
                    left: 5% !important;
                }
            }
        </style>
        """
        
        # Add the script and CSS to the map
        myanmar_map.get_root().html.add_child(Element(click_script))
        myanmar_map.get_root().html.add_child(Element(custom_css))

        # Add Bootstrap for dashboard styling
        bootstrap_css = Element(
            """
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">
            """
        )
        myanmar_map.get_root().html.add_child(bootstrap_css)

        # Set the figure dimensions
        figure = myanmar_map.get_root()
        figure.width = "100%"
        figure.height = "100%"
        
        # Render to HTML string
        geo_html = myanmar_map._repr_html_()
        
        context["html_code"] = geo_html
        return context

class MapClassView3(TemplateView):
    template_name = "maplayers/mapPage3.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dummy_map_data = DUMMY_DATA

        data = get_json_from_url("https://geonode.themimu.info/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_polbnda_adm3_250k_mimu_1&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature")

        if data is None:
            data = dummy_map_data

        # Initialize map centered on Myanmar
        myanmar_map = Map(
            location=[20.6303, 96.5617], 
            tiles="cartodb positron", 
            zoom_start=5,
            zoom_control=False,
            scroll_wheel_zoom=False,
            touch_zoom=False,
            width="100%",
            height=600,
        )
        
        # Create a feature group for each layer type
        feature_groups = {}
        
        # Create a mapping of properties for each feature to use in interactions
        feature_properties_js = {}
        
        # Process each feature in the GeoJSON
        for i, feature in enumerate(data.get('features', [])):
            # Extract properties for popup content
            properties = feature.get('properties', {})
            
            # Store feature properties in a JavaScript-accessible format
            feature_id = f"feature_{i}"
            # Convert properties to JSON string for JS
            feature_properties_js[feature_id] = json.dumps(properties)
            
            # Determine layer type
            layer_type = properties.get('type', 'default')
            
            # Create feature group if it doesn't exist
            if layer_type not in feature_groups:
                feature_groups[layer_type] = FeatureGroup(name=layer_type)
            
            # Create popup content from properties
            popup_html = "<div style='width: 200px;'>"
            for key, value in properties.items():
                popup_html += f"<strong>{key}:</strong> {value}<br>"
            popup_html += "</div>"
            
            # Default color for this feature
            default_color = properties.get('color', '#3388ff')
            
            # Add the feature to the map with popup
            geo_json = GeoJson(
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
                popup=Popup(popup_html, max_width=300),
                tooltip=properties.get('name', 'Click for more info')
            )
            
            # Add feature_id as a class to identify this feature
            geo_json.add_child(Element(f"<script>document.currentScript.parentElement.feature_id = '{feature_id}';</script>"))
            
            geo_json.add_to(feature_groups[layer_type])
        
        # Add each feature group to the map
        for group in feature_groups.values():
            group.add_to(myanmar_map)
        
        # Add layer control
        LayerControl().add_to(myanmar_map)
        
        # Generate sample regional data for interactive updates
        region_data_js = {
            "default": {
                "metrics": {
                    "total_sales": 1250,
                    "growth": "+15%",
                    "customers": 450,
                    "satisfaction": "4.8/5"
                },
                "line_data": {
                    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                    "sales": [5, 20, 36, 10, 75, 90],
                    "revenue": [15, 25, 40, 23, 55, 65]
                },
                "bar_data": {
                    "products": ["Product A", "Product B", "Product C", "Product D"],
                    "sales": [57, 134, 137, 129]
                }
            }
        }
        
        # Generate some regional variations for demo purposes
        for i in range(10):
            region_id = f"feature_{i}"
            region_data_js[region_id] = {
                "metrics": {
                    "total_sales": random.randint(800, 2000),
                    "growth": f"+{random.randint(5, 25)}%",
                    "customers": random.randint(300, 600),
                    "satisfaction": f"{random.randint(40, 50)/10}/5"
                },
                "line_data": {
                    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                    "sales": [random.randint(5, 30) for _ in range(6)],
                    "revenue": [random.randint(15, 50) for _ in range(6)]
                },
                "bar_data": {
                    "products": ["Product A", "Product B", "Product C", "Product D"],
                    "sales": [random.randint(40, 150) for _ in range(4)]
                }
            }
        
        # Add JavaScript to handle click events, change colors, and update dashboard
        dashboard_js = f"""
        <script>
            // Store original colors and the currently selected feature
            var originalColors = {{}};
            var originalStyles = {{}};
            var selectedFeature = null;
            var highlightColor = '#FF4500';
            var featureProperties = {json.dumps(feature_properties_js)};
            var regionData = {json.dumps(region_data_js)};
            var currentRegionData = regionData['default'];
            var currentFilters = {{
                dateRange: 'Last 7 Days',
                region: 'All Regions',
                product: 'All Products'
            }};

            // Store original event handlers
            var originalHandlers = {{}};
            
            // Function to wait for Leaflet to be fully loaded
            function waitForLeaflet(callback) {{
                if (typeof L !== 'undefined') {{
                    callback();
                }} else {{
                    setTimeout(function() {{ waitForLeaflet(callback); }}, 100);
                }}
            }}
            
            // Update dashboard charts and metrics
            function updateDashboardData(regionId) {{
                // Get data for the selected region, or default if not found
                let data = regionData[regionId] || regionData['default'];
                
                // Update metrics on the left column
                document.getElementById('metric-sales').innerText = data.metrics.total_sales;
                document.getElementById('metric-growth').innerText = data.metrics.growth;
                document.getElementById('metric-customers').innerText = data.metrics.customers;
                document.getElementById('metric-satisfaction').innerText = data.metrics.satisfaction;
                
                // Update line chart
                if (window.lineChart) {{
                    // Update chart data
                    window.lineChart.setOption({{
                        xAxis: {{
                            data: data.line_data.months
                        }},
                        series: [
                            {{
                                name: 'Sales',
                                data: data.line_data.sales
                            }},
                            {{
                                name: 'Revenue',
                                data: data.line_data.revenue
                            }}
                        ]
                    }});
                }}
                
                // Update bar chart
                if (window.barChart) {{
                    // Update chart data
                    window.barChart.setOption({{
                        xAxis: {{
                            data: data.bar_data.products
                        }},
                        series: [
                            {{
                                name: 'Sales',
                                data: data.bar_data.sales
                            }}
                        ]
                    }});
                }}

                // Update selected region display if applicable
                const regionDisplay = document.getElementById('selected-region');
                if (regionDisplay) {{
                    if (regionId === 'default') {{
                        regionDisplay.innerText = 'All Regions';
                    }} else {{
                        let props = featureProperties[regionId];
                        if (props) {{
                            let properties = JSON.parse(props);
                            regionDisplay.innerText = properties.name || properties.NAME_3 || properties.ADM3_EN || 'Selected Region';
                        }} else {{
                            regionDisplay.innerText = 'Selected Region';
                        }}
                    }}
                }}

                console.log('Dashboard updated with data for region:', regionId);
            }}
            
            // Apply filters and update dashboard
            function applyFilters() {{
                // Get selected values
                currentFilters.dateRange = document.getElementById('dateRange').value;
                currentFilters.region = document.getElementById('region').value;
                currentFilters.product = document.getElementById('product').value;
                
                console.log('Applying filters:', currentFilters);
                
                // For demonstration purposes, we'll just modify the data by some factor
                let modifiedData = null;
                
                // Date range factors
                let dateRangeFactor = 1.0;
                if (currentFilters.dateRange === 'Last 30 Days') dateRangeFactor = 1.5;
                if (currentFilters.dateRange === 'Last 90 Days') dateRangeFactor = 2.5;
                if (currentFilters.dateRange === 'Custom Range') dateRangeFactor = 3.0;
                
                // Region factors
                let regionFactor = 1.0;
                if (currentFilters.region === 'North America') regionFactor = 1.8;
                if (currentFilters.region === 'Europe') regionFactor = 1.4;
                if (currentFilters.region === 'Asia-Pacific') regionFactor = 1.6;
                
                // Product factors
                let productFactor = 1.0;
                if (currentFilters.product !== 'All Products') productFactor = 1.2;
                
                // Total factor
                let factor = dateRangeFactor * regionFactor * productFactor;
                
                // Get current region ID
                let regionId = selectedFeature ? selectedFeature.feature_id || 'default' : 'default';
                let baseData = regionData[regionId] || regionData['default'];
                
                // Create modified data
                modifiedData = JSON.parse(JSON.stringify(baseData)); // Deep clone
                
                // Apply factors to data
                modifiedData.metrics.total_sales = Math.round(baseData.metrics.total_sales * factor);
                modifiedData.metrics.customers = Math.round(baseData.metrics.customers * factor);
                
                // Growth depends on date range
                let growthValue = parseFloat(baseData.metrics.growth) * dateRangeFactor;
                modifiedData.metrics.growth = '+' + growthValue.toFixed(1) + '%';
                
                // Apply to charts
                for (let i = 0; i < modifiedData.line_data.sales.length; i++) {{
                    modifiedData.line_data.sales[i] = Math.round(baseData.line_data.sales[i] * factor);
                    modifiedData.line_data.revenue[i] = Math.round(baseData.line_data.revenue[i] * factor);
                }}
                
                for (let i = 0; i < modifiedData.bar_data.sales.length; i++) {{
                    modifiedData.bar_data.sales[i] = Math.round(baseData.bar_data.sales[i] * factor);
                }}
                
                // Update charts with modified data
                // Update metrics on the left column
                document.getElementById('metric-sales').innerText = modifiedData.metrics.total_sales;
                document.getElementById('metric-growth').innerText = modifiedData.metrics.growth;
                document.getElementById('metric-customers').innerText = modifiedData.metrics.customers;
                document.getElementById('metric-satisfaction').innerText = modifiedData.metrics.satisfaction;
                
                // Update line chart
                if (window.lineChart) {{
                    window.lineChart.setOption({{
                        xAxis: {{
                            data: modifiedData.line_data.months
                        }},
                        series: [
                            {{
                                name: 'Sales',
                                data: modifiedData.line_data.sales
                            }},
                            {{
                                name: 'Revenue',
                                data: modifiedData.line_data.revenue
                            }}
                        ]
                    }});
                }}
                
                // Update bar chart
                if (window.barChart) {{
                    window.barChart.setOption({{
                        xAxis: {{
                            data: modifiedData.bar_data.products
                        }},
                        series: [
                            {{
                                name: 'Sales',
                                data: modifiedData.bar_data.sales
                            }}
                        ]
                    }});
                }}

                document.getElementById('filter-status').innerText = 
                    `Applied filters: ${{currentFilters.dateRange}} | ${{currentFilters.region}} | ${{currentFilters.product}}`;
            }}
            
            // Main initialization function for map interactions
            function initializeClickHandlers() {{
                // Get all map containers
                var mapContainers = document.querySelectorAll('.folium-map');
                
                if (mapContainers.length === 0) {{
                    // If map isn't ready yet, try again later
                    setTimeout(initializeClickHandlers, 500);
                    return;
                }}
                
                // Get the first map container (there's usually only one)
                var mapContainer = mapContainers[0];
                
                // Get the Leaflet map instance
                var leafletMap = window._leaflet_map || window.leafletMap;
                
                if (!leafletMap) {{
                    console.log("Searching for map instance...");
                    // Try to find the map by searching through global variables
                    for (var key in window) {{
                        if (window[key] && 
                            typeof window[key] === 'object' && 
                            window[key] instanceof L.Map) {{
                            leafletMap = window[key];
                            console.log("Found map instance:", key);
                            break;
                        }}
                    }}
                }}
                
                if (!leafletMap) {{
                    console.log("Map not ready yet, retrying...");
                    setTimeout(initializeClickHandlers, 500);
                    return;
                }}
                
                console.log("Map instance found, setting up click handlers");
                
                // Function to reset previous selection
                function resetSelection() {{
                    if (selectedFeature) {{
                        var originalStyle = originalStyles[selectedFeature._leaflet_id];
                        if (originalStyle) {{
                            selectedFeature.setStyle(originalStyle);
                        }}

                        // Restore the original event handlers if they exist
                        if (originalHandlers[selectedFeature._leaflet_id]) {{
                            var handlers = originalHandlers[selectedFeature._leaflet_id];

                            // Re-enable mouseover hander if it existed
                            if (handlers.mouseover) {{
                                selectedFeature.on('mouseover', handlers.mouseover);
                            }}

                            // Re-enable mouseout handler if it existed
                            if (handlers.mouseout) {{
                                selectedFeature.on('mouseout', handlers.mouseout);
                            }}

                            // Clear stored handlers
                            delete originalHandlers[selectedFeature._leaflet_id];
                        }}

                        selectedFeature = null;
                    }}
                }}
                
                // Add click handlers to all GeoJSON layers
                leafletMap.eachLayer(function(layer) {{
                    // Only process GeoJSON layers
                    if (layer.feature && layer.setStyle) {{
                        // Store original color
                        var style = layer.options || {{}};
                        originalColors[layer._leaflet_id] = style.fillColor || '#3388ff';
                        originalStyles[layer._leaflet_id] = JSON.parse(JSON.stringify(style));

                        // Add click handler
                        layer.on('click', function(e) {{
                            console.log("Layer clicked");
                            
                            // Reset previous selection
                            resetSelection();
                            
                            // Highlight this feature
                            selectedFeature = e.target;
                            
                            // Store original event handlers before removing them
                            originalHandlers[selectedFeature._leaflet_id] = {{
                                mouseover: e.target._events && e.target._events.mouseover ?
                                            e.target._events.mouseover[0].fn : null,
                                mouseout: e.target._events && e.target._events.mouseout ?
                                            e.target._events.mouseout[0].fn : null
                            }};

                            // Temporarily disable mouseover/mouseout for this layer only
                            e.target.off('mouseover');
                            e.target.off('mouseout');
                            
                            // Apply highlight style
                            e.target.setStyle({{
                                fillColor: highlightColor,
                                fillOpacity: 0.9,
                                weight: 3
                            }});

                            // Bring to front (for overlapping polygons)
                            if (e.target.bringToFront) {{
                                e.target.bringToFront();
                            }}
                            
                            // Get feature ID for this layer
                            let featureId = e.target.feature_id || 'default';
                            console.log("Feature ID:", featureId);
                            
                            // Update dashboard with this region's data
                            updateDashboardData(featureId);
                            
                            // Also apply any current filters
                            applyFilters();
                            
                            // Prevent click from propagating
                            if (e.originalEvent) {{
                                L.DomEvent.stopPropagation(e.originalEvent);
                            }}
                        }});

                        // Store feature_id on the layer if present
                        if (layer.feature_id) {{
                            layer.feature_id = layer.feature_id;
                        }}
                    }}
                }});
                
                // Reset selection when clicking map background
                leafletMap.on('click', function() {{
                    resetSelection();
                    // Reset to default data
                    updateDashboardData('default');
                    // Apply filters to default data
                    applyFilters();
                }});
                
                console.log("Click handlers initialized");
            }}

            // Initialize charts after DOM is loaded
            function initializeCharts() {{
                // Initialize line chart
                window.lineChart = echarts.init(document.getElementById('line-chart'));
                window.lineChart.setOption({{
                    title: {{ text: 'Monthly Performance' }},
                    tooltip: {{ trigger: 'axis' }},
                    legend: {{ data: ['Sales', 'Revenue'] }},
                    xAxis: {{ type: 'category', data: currentRegionData.line_data.months }},
                    yAxis: {{ type: 'value' }},
                    series: [
                        {{
                            name: 'Sales',
                            type: 'line',
                            data: currentRegionData.line_data.sales,
                            smooth: true
                        }},
                        {{
                            name: 'Revenue',
                            type: 'line',
                            data: currentRegionData.line_data.revenue,
                            smooth: true
                        }}
                    ]
                }});

                // Initialize bar chart
                window.barChart = echarts.init(document.getElementById('bar-chart'));
                window.barChart.setOption({{
                    title: {{ text: 'Product Performance' }},
                    tooltip: {{ trigger: 'axis' }},
                    xAxis: {{ type: 'category', data: currentRegionData.bar_data.products }},
                    yAxis: {{ type: 'value' }},
                    series: [
                        {{
                            name: 'Sales',
                            type: 'bar',
                            data: currentRegionData.bar_data.sales
                        }}
                    ]
                }});

                // Handle window resize
                window.addEventListener('resize', function() {{
                    if (window.lineChart) window.lineChart.resize();
                    if (window.barChart) window.barChart.resize();
                }});
            }}
            
            // Wait for Leaflet and DOM to be ready
            document.addEventListener('DOMContentLoaded', function() {{
                console.log("DOM loaded, waiting for Leaflet");
                
                // Initialize filter controls
                document.getElementById('apply-filters').addEventListener('click', applyFilters);
                
                // Initialize charts
                if (typeof echarts !== 'undefined') {{
                    initializeCharts();
                }} else {{
                    console.error("ECharts not loaded");
                }}
                
                // Initialize map interactions
                waitForLeaflet(function() {{
                    console.log("Leaflet loaded, initializing handlers");
                    // Give extra time for Folium to finish rendering
                    setTimeout(initializeClickHandlers, 1000);
                }});
            }});
        </script>
        """

        custom_css = """
        <style>
            .leaflet-interactive {
                transition: fill 0.3s ease, stroke-width 0.3s ease;
            }
            .folium-map {
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
            }
            .stats-card {
                transition: all 0.3s ease;
            }
            .stats-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }
        </style>
        """
        
        # Add the script and CSS to the map
        myanmar_map.get_root().html.add_child(Element(dashboard_js))
        myanmar_map.get_root().html.add_child(Element(custom_css))

        figure = myanmar_map.get_root()
        figure.width = "100%"
        figure.height = "100%"
        
        # Render to HTML string
        geo_html = myanmar_map._repr_html_()  # Render map as HTML

        # Example data for text boxes
        metrics = {
            'total_sales': 1250,
            'growth': '+15%',
            'customers': 450,
            'satisfaction': '4.8/5'
        }

        # Generate the complete HTML for the dashboard using Bootstrap classes
        dashboard_html = f"""
        <!-- Include ECharts library -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
        
        <!-- Dashboard Content using Bootstrap classes -->
        <div class="container-fluid">
            <!-- Top Row - Controls -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card bg-light">
                        <div class="card-body">
                            <h4 class="card-title">Dashboard Controls</h4>
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="dateRange">Date Range</label>
                                        <select class="form-control" id="dateRange">
                                            <option>Last 7 Days</option>
                                            <option>Last 30 Days</option>
                                            <option>Last 90 Days</option>
                                            <option>Custom Range</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="region">Region Focus</label>
                                        <select class="form-control" id="region">
                                            <option>All Regions</option>
                                            <option>North America</option>
                                            <option>Europe</option>
                                            <option>Asia-Pacific</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label for="product">Product</label>
                                        <select class="form-control" id="product">
                                            <option>All Products</option>
                                            <option>Product A</option>
                                            <option>Product B</option>
                                            <option>Product C</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group">
                                        <label>&nbsp;</label>
                                        <button id="apply-filters" class="btn btn-primary form-control">Apply Filters</button>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-3">
                                <div id="filter-status" class="text-muted">Applied filters: Last 7 Days | All Regions | All Products</div>
                                <div class="mt-2">
                                    <strong>Selected Region: </strong><span id="selected-region">All Regions</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Bottom Row - Main Dashboard Content -->
            <div class="row">
                <!-- Left Column - Text Boxes -->
                <div class="col-md-3">
                    <div class="card h-100">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Key Metrics</h5>
                        </div>
                        <div class="card-body">
                            <div class="bg-light p-3 rounded mb-3 shadow-sm stats-card">
                                <div class="text-muted">Total Sales</div>
                                <div id="metric-sales" class="h4 mb-0">{metrics['total_sales']}</div>
                            </div>
                            <div class="bg-light p-3 rounded mb-3 shadow-sm stats-card">
                                <div class="text-muted">Growth Rate</div>
                                <div id="metric-growth" class="h4 mb-0">{metrics['growth']}</div>
                            </div>
                            <div class="bg-light p-3 rounded mb-3 shadow-sm stats-card">
                                <div class="text-muted">Active Customers</div>
                                <div id="metric-customers" class="h4 mb-0">{metrics['customers']}</div>
                            </div>
                            <div class="bg-light p-3 rounded mb-3 shadow-sm stats-card">
                                <div class="text-muted">Satisfaction Score</div>
                                <div id="metric-satisfaction" class="h4 mb-0">{metrics['satisfaction']}</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Middle Column - Map -->
                <div class="col-md-5">
                    <div class="card h-100">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Geographic Distribution</h5>
                        </div>
                        <div class="card-body">
                            <div id="map-container" style="height:400px;">
                                {geo_html}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Right Column - Charts -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Performance Analytics</h5>
                        </div>
                        <div class="card-body">
                            <div id="line-chart" style="height:200px;" class="mb-3"></div>
                            <div id="bar-chart" style="height:200px;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        context["html_code"] = geo_html
        context["dashboard_html"] = dashboard_html

        return context