import json
from os.path import abspath, dirname, join

import mbta

RESOURCES_DIRECTORY = join(abspath(dirname(__file__)), "resources")


def test_from_json():
    with open(join(RESOURCES_DIRECTORY, "route.json"), "r") as f:
        route_data = json.load(f)["data"][0]
    route = mbta.route._from_json(route_data)
    assert route.id == route_data["id"]
    assert route.name == route_data["attributes"]["long_name"]
    assert route.directions == [
        {
            "name": route_data["attributes"]["direction_names"][0],
            "destination": route_data["attributes"]["direction_destinations"][0],
        },
        {
            "name": route_data["attributes"]["direction_names"][1],
            "destination": route_data["attributes"]["direction_destinations"][1],
        },
    ]
    assert route.type == route_data["attributes"]["type"]
