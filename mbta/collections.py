from typing import Any, Dict, List, Set, Union
from mbta.station import Station


class TransferRouteError(
    Exception
):  # custom exception for a failure to find a transfer route between two stations.
    pass


def all_stations(routes: Dict[str, Any]) -> Dict[str, Dict[str, Union[Station, Set[str]]]]:
    """
    Takes a grouping of routes with their stations, and returns a station-centric view of all stations in the given
    routes as well as all routes each station serves.
    :param routes: Routes from which to aggregate stations
    :return: Dictionary of all stations, keyed by station-id, with the Station object and the routes each serves.
    """
    stations = {}
    for route in routes:
        for station in routes[route]["stations"]:
            stations[station.id] = {
                "station": station,
                "lines": stations.get(station.id, {}).get("lines", []) + [route],
            }
    for key, value in stations.items():
        stations[key]["lines"] = set(value["lines"])
    return stations


def transfer_stations(
    stations: Dict[str, Dict[str, Union[Station, Set[str]]]]
) -> Dict[str, Dict[str, Union[Station, Set[str]]]]:
    """
    Returns all stations which serve more than one route.
    :param stations:
    :return:
    """
    return {key: value for key, value in stations.items() if len(value["lines"]) > 1}


def line_transfers(
    tx_stations: Dict[str, Dict[str, Union[Station, Set[str]]]],
    down_lines: List[str] = [],
) -> Dict[str, List[Dict[str, str]]]:
    """
    Returns all route-route transfer connections and the stations at which to transfer.
    :param tx_stations: All stations which serve more than one route.
    :return:
    """
    routes = {down_line: [] for down_line in down_lines}
    for station in tx_stations:
        lines = tx_stations[station]["lines"]
        for line in lines:
            if line not in down_lines:
                routes[line] = routes.get(line, []) + [
                    {"line": transfer_line, "station": station}
                    for transfer_line in lines
                    if (transfer_line != line and transfer_line not in down_lines)
                ]
    return routes


def connection(
    origin: Dict[str, Union[Station, Set[str]]],
    destination: Dict[str, Union[Station, Set[str]]],
    line_transfers: Dict[str, List[Dict[str, str]]],
) -> Dict[str, List[str]]:
    """
    Computes transfer route between two stations
    :param origin:
    :param destination:
    :param line_transfers:
    :return:
    """
    direct = list(origin["lines"] & destination["lines"])
    if len(direct) > 0:
        return {"lines": [direct[0]], "transfer_stations": [destination["station"].id]}
    for line in origin["lines"]:
        for transfer in line_transfers[line]:
            if transfer["line"] in destination["lines"]:
                return {
                    "lines": [line, transfer["line"]],
                    "transfer_stations": [transfer["station"], destination["station"].id],
                }
    for line in origin["lines"]:
        for transfer in line_transfers[line]:
            for second_transfer in line_transfers[transfer["line"]]:
                if second_transfer["line"] in destination["lines"]:
                    return {
                        "lines": [line, transfer["line"], second_transfer["line"]],
                        "transfer_stations": [
                            transfer["station"],
                            second_transfer["station"],
                            destination["station"].id,
                        ],
                    }
    for line in origin["lines"]:
        for transfer in line_transfers[line]:
            for second_transfer in line_transfers[transfer["line"]]:
                for third_transfer in line_transfers[second_transfer["line"]]:
                    if third_transfer["line"] in destination["lines"]:
                        return {
                            "lines": [
                                line,
                                transfer["line"],
                                second_transfer["line"],
                                third_transfer["line"],
                            ],
                            "transfer_stations": [
                                transfer["station"],
                                second_transfer["station"],
                                third_transfer["station"],
                                destination["station"].id,
                            ],
                        }
    raise TransferRouteError
