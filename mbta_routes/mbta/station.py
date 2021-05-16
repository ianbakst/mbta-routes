from dataclasses import dataclass
import requests
from typing import Any, Dict, Set

from mbta.route import Route


BASE_PATH = "https://api-v3.mbta.com"


@dataclass(frozen=True)
class Station:  # Object representation of a Station
    id: str
    name: str


def get_all_from_route(route: Route) -> Set[Station]:
    """
    Get all stations on a given route.
    e.g. Red Line -> Kendall, Davis, Porter, etc.
    :param route: Route object on which to get stations
    :return: Station objects for each station on the route.
    """
    r = requests.get(
        f"{BASE_PATH}/routes/{route.id}?include=route_patterns.representative_trip.stops"
    )
    return _all_from_json(r.json())


def _all_from_json(data: Dict[str, Any]) -> Set[Station]:
    """
    Build the set of stations in a given route from data in the route relationship query
    :param data: Json Dict of route relationship
    :return: Set of Stations on a route
    """
    route_patterns = {}
    representative_trips = {}
    stops = {}
    try:
        for item in data["included"]:
            if item["type"] == "stop":
                stops[item["id"]] = item
            elif item["type"] == "route_pattern":
                route_patterns[item["id"]] = item
            elif item["type"] == "trip":
                representative_trips[item["id"]] = item
            else:
                raise ValueError
    except KeyError:
        print("API throttling reached. Please wait a minute and try again.")
        raise
    stations = []
    for route_pattern in data["data"]["relationships"]["route_patterns"]["data"]:
        trip_id = route_patterns[route_pattern["id"]]["relationships"]["representative_trip"][
            "data"
        ]["id"]
        trip = representative_trips[trip_id]
        stations.extend(
            [_from_json(stops[s["id"]]) for s in trip["relationships"]["stops"]["data"]]
        )
    return set(stations)


def _from_json(data: Dict[str, Any]) -> Station:
    """
    Build Station object from json dictionary of data.
    :param data: Json Dict with data about the station.
    :return: Station object
    """
    return Station(
        data["relationships"]["parent_station"]["data"]["id"],
        data["attributes"]["name"],
    )
