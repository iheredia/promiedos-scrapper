from .helpers import write_json, read_json, files_in_dir
from .match import Match
import progressbar


def read_files(data_dir):
    raw_matches = []
    files_bar = progressbar.ProgressBar()
    for file_path in files_bar(files_in_dir(data_dir)):
        raw_matches += read_json(file_path)
    return raw_matches


def create_instances(raw_matches):
    matches = []
    match_bar = progressbar.ProgressBar()
    for raw_match in match_bar(raw_matches):
        matches.append(Match(raw_match))

    coordinates_bar = progressbar.ProgressBar()
    matches_with_coordinates = [m for m in matches if m.obj['lugar'] is not None]
    for match in coordinates_bar(matches_with_coordinates):
        match.get_coordinates()
    return matches


def remove_duplicates(matches):
    sorted_matches = sorted(matches, key=lambda m: m.raw)
    unique_matches = [sorted_matches[0]]
    unique_bar = progressbar.ProgressBar()
    for i in unique_bar(range(1, len(sorted_matches))):
        if sorted_matches[i] != sorted_matches[i - 1]:
            unique_matches.append(sorted_matches[i])
    return unique_matches


def parse_promedios_data(data_dir):
    raw_matches = read_files(data_dir)
    matches = create_instances(raw_matches)
    unique_matches = remove_duplicates(matches)
    argentina = [m.obj for m in unique_matches if m.includes_argentina]
    national = [m.obj for m in unique_matches if not m.includes_argentina]
    write_json(argentina, 'data/argentina.json')
    write_json(national, 'data/nacional.json')
