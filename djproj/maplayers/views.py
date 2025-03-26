import json
import requests
from django.shortcuts import render

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
    dummy_map_data = {
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

    data = get_json_from_url("https://geonode.themimu.info/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_polbnda_adm3_250k_mimu_1&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature")

    if data is None:
        data = dummy_map_data
    
    # Convert to JSON and ensure it's safe to use in templates
    context = {
        'map_data': json.dumps(data)
    }
    
    return render(request, "maplayers/mapPage.html", context)

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