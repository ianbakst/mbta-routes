from datetime import datetime
import logging

import mbta


# Setting up Logger to log to console but also log to file.
file_handler = logging.FileHandler(f'logs/{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.log')
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s:%(message)s"))

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(message)s"))

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler],
)

LOGGER = logging.getLogger()

# a function to print stations' names and their ids
def print_all_stations(all_stations):
    for station in all_stations.values():
        print(f"Station Name: {station['station'].name}, Station ID: '{station['station'].id}'.")


def main():
    down_lines = ["Orange", "Green-B", "Green-C", "Green-D", "Green-E"]
    running = True  # for the while loop
    # Get and build the data structures for all operations.
    mode = '0'
    while running:
        # Switch for program actions
        if mode == '0':
            routes = mbta.route.get_all([0, 1])
            for r in routes.values():
                route_stations = mbta.station.get_all_from_route(r["route"])
                routes[r["route"].id]["stations"] = route_stations
                routes[r["route"].id]["num_stops"] = len(route_stations)
            all_stations = mbta.all_stations(routes)
            tx_stations = mbta.transfer_stations(all_stations)
            itx = mbta.line_transfers(tx_stations)

        elif mode == '1':
            # display route names
            LOGGER.info("All 'Light Rail' and 'Heavy Rail' route names:")
            for r in routes.values():
                LOGGER.info(r["route"].name)

        elif mode == '2':
            # find route with most stops, display result.
            most_stops = max(routes.items(), key=lambda v: routes[v[0]]["num_stops"])[0]
            LOGGER.info(
                f"The {routes[most_stops]['route'].name} has the most stops with {routes[most_stops]['num_stops']}."
            )

        elif mode == '3':
            # find route with fewest stops, display result
            fewest_stops = min(routes.items(), key=lambda v: routes[v[0]]["num_stops"])[0]
            LOGGER.info(
                f"The {routes[fewest_stops]['route'].name} has the fewest stops with {routes[fewest_stops]['num_stops']}."
            )

        elif mode == '4':
            # display all stations with transfers
            for tx_station in tx_stations.values():
                LOGGER.info(
                    f"{tx_station['station'].name} connects the routes: {', '.join([routes[line]['route'].name for line in tx_station['lines']])}"
                )

        elif mode == '5':
            # choose origin id and destination id
            origin_id = None
            dest_id = None
            while origin_id is None:
                # ask for origin id, ensure it's valid, provide help
                origin_id = input(
                    'Please provide the station-id of your origin: (type "help" to view station ids)'
                )
                if origin_id.lower() == "help":
                    print_all_stations(all_stations)
                    origin_id = None
                elif origin_id not in all_stations.keys():
                    print("Origin ID invalid, please provide a valid origin ID.")
                    origin_id = None
            while dest_id is None:
                # ask for destination id, ensure it's valid, provide help
                dest_id = input(
                    'Please provide the station-id of your destination: (type "help" to view station ids)'
                )
                if dest_id.lower() == "help":
                    print_all_stations(all_stations)
                    dest_id = None
                elif dest_id not in all_stations.keys():
                    print("Destination ID invalid, please provide a valid destination ID.")
                    dest_id = None

            try:
                cnxn = mbta.connection(all_stations[origin_id], all_stations[dest_id], itx)
                connection_string = " Then ".join(
                    [
                        f"take the {routes[line]['route'].name} to {all_stations[cnxn['transfer_stations'][i]]['station'].name}."
                        for i, line in enumerate(cnxn["lines"])
                    ]
                )
                LOGGER.info(f"From {all_stations[origin_id]['station'].name} {connection_string}")
            except mbta.collections.TransferRouteError:
                LOGGER.warning(f"Cannot find route transfer. The following lines are down: {', '.join([routes[d]['route'].name for d in down_lines])}.")

        elif mode == '6':
            LOGGER.info("Exiting program.")
            running = False
        else:
            LOGGER.info("Invalid option chosen. Please choose between 1-6.")

        # Choose which action
        mode = input(
            "What would you like the know?\n"
            "(1) - All Light Rail and Heavy Rail route names\n"
            "(2) - Route with the most stops.\n"
            "(3) - Route with the fewest stops.\n"
            "(4) - All stations which connect multiple subway routes.\n"
            "(5) - Transfers between two stations.\n"
            "(6) - Exit.\n"
            "(0) - Refresh data.\n")
    return


if __name__ == "__main__":
    main()
