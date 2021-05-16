from dataclasses import dataclass
import requests
from requests import Response
from typing import Any, Dict, List, Union

BASE_PATH = "https://api-v3.mbta.com"


@dataclass(frozen=True)
class Route:
    # Object represenation of an MBTA route
    id: str
    name: str
    directions: List[Dict[str, str]]
    type: int


def _from_json(data: Dict[str, Any]) -> Route:
    """
    Build Route object from json data.
    :param data: Json dictonary with data about route.
    :return: Route object.
    """
    return Route(
        data["id"],
        data["attributes"]["long_name"],
        [
            {"name": d_name, "destination": data["attributes"]["direction_destinations"][i]}
            for i, d_name in enumerate(data["attributes"]["direction_names"])
        ],
        data["attributes"]["type"],
    )


def _get_routes(url: str = "/routes") -> Response:
    """
    Call api to get routes with given endpoint filters.
    :param url: Endpoint specifying filters
    :return: request response from API call
    """
    return requests.get(f"{BASE_PATH}{url}")


def get_all(route_types: Union[List[int], int, None] = None) -> Dict[str, Dict[str, Route]]:
    """
    Get all route data from given route types. Default is ALL ROUTES.
    Passing a single integer will get data for that route type.
    Passing a list of integers will get data for all route types in the list.
    :param route_types: List of route types, a single route type, or None (all routes).
    :return: Route objects in dictionary keyed on route id:
    {<route_id>: {"route": <Route object>}}
    """
    if isinstance(route_types, int):
        route_types = [route_types]
    api_url = "/routes"
    if route_types:
        api_url = f"{api_url}?filter[type]={','.join([str(r) for r in route_types])}"
    req = _get_routes(api_url)
    if req.status_code >= 400:
        raise ValueError
    if len(req.json()['data']) == 0:
        raise ValueError(f"Invalid route type(s) {route_types}.")
    return {d["id"]: {"route": _from_json(d)} for d in req.json().pop("data")}
