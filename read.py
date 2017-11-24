import os
import json


def read_all_matches():
    matches = []
    for file_name in os.listdir('tmp'):
        with open('tmp/' + file_name, 'r') as json_file:
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
        json.dump(obj, json_file, ensure_ascii=False)


if __name__ == '__main__':
    all_matches = remove_duplicates(read_all_matches())
    argentina, national = separate_argentina(all_matches)
    save_json(argentina, 'data/argentina.json')
    save_json(national, 'data/nacional.json')
