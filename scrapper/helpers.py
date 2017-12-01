import json
import os
import re
import requests


def read_json(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)


def write_json(obj, path, **kw):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    params = {'ensure_ascii': False, 'indent': 2}
    params.update(kw)
    with open(path, 'w') as json_file:
        json.dump(obj, json_file, **params)


def files_in_dir(path_to_dir):
    file_paths = []
    for filename in os.listdir(path_to_dir):
        file_path = os.path.join(path_to_dir, filename)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths


def parse_date(date_string):
    date = re.findall('\d{2}/\d{2}/\d{4}', date_string)
    if len(date) == 0:
        return None
    if len(date) > 1:
        print('Warning: more than 1 date at ', date_string)
    return '/'.join(date[0].split('/')[::-1])


def _get_coordinates(query_string, region_ar=True):
    if region_ar:
        path_to_cache = 'tmp/geolocation_ar_%s.json' % query_string
    else:
        path_to_cache = 'tmp/geolocation_%s.json' % query_string
    if os.path.isfile(path_to_cache):
        response = read_json(path_to_cache)
    else:
        params = {"address": query_string}
        if region_ar:
            params['region'] = 'ar'
        # https://developers.google.com/maps/documentation/geocoding/intro?hl=es-419
        api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        response = requests.get(api_url, params=params).json()
        write_json(response, path_to_cache)
    lat, long = None, None
    results = response.get('results', [])
    if len(results) > 0:
        if len(results) > 1:
            print('Got %d results for %s' % (len(results), query_string))
        location = results[0].get('geometry', {}).get('location', {})
        lat = location.get('lat', None)
        long = location.get('lng', None)
    return lat, long


def get_coordinates(query_string):
    lat, long = _get_coordinates(query_string)
    if lat is None:
        lat, long = _get_coordinates(query_string, region_ar=False)
    return lat, long
