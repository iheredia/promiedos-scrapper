import os
import json
import re
import requests


def read_all_matches():
    matches = []
    for file_name in os.listdir('tmp'):
        file_path = 'tmp/' + file_name
        if os.path.isfile(file_path):
            with open(file_path, 'r') as json_file:
                matches += json.load(json_file)
    return matches


def separate_argentina(matches):
    arg = []
    national_teams = []

    for m in matches:
        if m[0] == 'Argentina' or m[3] == 'Argentina':
            arg.append(m)
        else:
            national_teams.append(m)

    return arg, national_teams


def remove_duplicates(matches):
    def matches_are_equal(m1, m2):
        return len(m1) == len(m2) and all([m1[i] == m2[i] for i in range(len(m1))])

    sorted_alphabetically = sorted(matches)
    return [sorted_alphabetically[0]] + [
        sorted_alphabetically[i]
        for i in range(1, len(sorted_alphabetically))
        if not matches_are_equal(sorted_alphabetically[i], sorted_alphabetically[i-1])
    ]


def parse_date(date_string):
    date = re.findall('\d{2}/\d{2}/\d{4}', date_string)
    if len(date) == 0:
        return None
    if len(date) > 1:
        print('Warning: more than 1 date at ', date_string)
    return '/'.join(date[0].split('/')[::-1])


def to_obj(match):
    if '(' in match[1]:
        team1_scores = re.findall('\d+', match[1])
        score1 = int(team1_scores[0])
        penalty1 = int(team1_scores[1])

        team2_scores = re.findall('\d+', match[2])
        score2 = int(team2_scores[0])
        penalty2 = int(team2_scores[1])

        penalties = [penalty1, penalty2]
    else:
        penalties = None
        score1 = int(match[1])
        score2 = int(match[2])

    place = None
    if 'En' in match[4]:
        place = match[4].split('En ')[1].strip()

    match_type = None
    if '-' in match[4]:
        match_type = match[4].split('-')[0].strip()

    return {
        'equipos': [match[0], match[3]],
        'resultado': [score1, score2],
        'penales': penalties,
        'fecha': parse_date(match[4]),
        'lugar': place,
        'tipo': match_type,
        'raw': match[4]
    }


def compress(matches):
    teams_set = set()
    scores_set = set()
    for m in matches:
        teams_set.add(m[0])
        scores_set.add(m[1])
        scores_set.add(m[2])
        teams_set.add(m[3])
    teams = sorted(list(teams_set))
    scores = sorted(list(scores_set))
    return {
        'equipos': teams,
        'puntajes': scores,
        'partidos': [
            [
                teams.index(m[0]),
                scores.index(m[1]),
                scores.index(m[2]),
                teams.index(m[3]),
                m[4]
            ]
            for m in matches
        ]
    }


def save_json(obj, path):
    with open(path, 'w') as json_file:
        json.dump(obj, json_file, ensure_ascii=False, indent=2)


def parse_national_raw(match):
    before, after = match['raw'].rsplit(' -')

    before = before.strip()
    rindex = before.rindex(' ')
    name = before[:rindex].strip()
    period = before[rindex + 1:].strip()

    if len(after) == 0:
        after = None
    else:
        after = after.strip()
    match['torneo'] = {
        'nombre': name,
        'periodo': period,
        'contexto': after
    }

    del match['raw']
    return match


def coordinates(query_string):
    path_to_cache = 'tmp/geolocation/geolocation_%s.json' % query_string
    if os.path.isfile(path_to_cache):
        with open(path_to_cache, 'r') as response_json_file:
            response = json.load(response_json_file)
    else:
        params = {
            "address": query_string
        }
        api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        response = requests.get(api_url, params=params).json()
        with open(path_to_cache, 'w') as response_json_file:
            json.dump(response, response_json_file)
    lat, long = None, None
    results = response.get('results', [])
    if len(results) > 0:
        if len(results) > 1:
            print('Got %d results for %s' % (len(results), query_string))
        location = results[0].get('geometry', {}).get('location', {})
        lat = location.get('lat', None)
        long = location.get('lng', None)
    return lat, long


def with_coordinates(match):
    lat, long = coordinates(match['lugar'])
    match["lugar"] = {
        "raw": match["lugar"],
        "lat": lat,
        "long": long
    }
    return match


if __name__ == '__main__':
    all_matches = remove_duplicates(read_all_matches())
    argentina, national = separate_argentina(all_matches)

    argentina = [to_obj(m) for m in argentina]
    argentina = [with_coordinates(m) for m in argentina]

    national = [to_obj(m) for m in national]
    national = [parse_national_raw(m) for m in national]

    save_json(argentina, 'data/argentina.json')
    save_json(national, 'data/nacional.json')
