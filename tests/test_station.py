import json
from os.path import abspath, dirname, join

import mbta

RESOURCES_DIRECTORY = join(abspath(dirname(__file__)), 'resources')

def test_from_json():
    with open(join(RESOURCES_DIRECTORY, 'stop.json'), 'r') as f:
        stop_data = json.load(f)
    station = mbta.station._from_json(stop_data)
    assert station.id == stop_data["relationships"]["parent_station"]["data"]["id"]
    assert station.name == stop_data['attributes']['name']


def test_all_from_json():
    with open(join(RESOURCES_DIRECTORY,'red_line_station_query.json'), 'r') as f:
        red_line_data = json.load(f)
    stations = mbta.station._all_from_json(red_line_data)
    stop_data = [data for data in red_line_data['included'] if data['type'] == 'stop'][0]
    for station in stations:
        assert station.id == stop_data['relationships']['parent_station']['data']['id']
        assert station.name == stop_data['attributes']['name']