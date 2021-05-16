# MBTA Routes and Stops
A lightweight program for navigating the MBTA subway system.

### Quick Start
This program is ready to be built into a docker image and deployed immediately. To do so, follow these steps:
0. Be sure you have docker installed on your machine.
1. Build this in a docker container with the command `docker build -t <container_name> .` 
(execute this command in the top directory of this program).
2. Once the image is built, run the container with the command: `docker run -it <container_name>`
3. The program will now be running in the terminal.

### Developer Start
To develop, build a virtual environment: `python -m venv <virtual_environment_name>`.
Be sure to install the requirements as well as the dev requirements:
* `pip install -r requirements.txt`
* `pip install -r dev-requirements.txt`
* Install the MBTA package: `pip install .`

This package has tasks set up for formatting and linting. This can be performed by:
* Linting: `python -m invoke lint`
* Formatting: `python -m invoke format` (add `--fix` to automatically fix formatting when running).

Additionally, you can perform unit tests with the command `pytest`. Tests are located in the `tests` directory,
with relevant resources located in the `tests/resources` directory.

### Usage
This program will run in the console and give you the option of 5 actions:
1. Display all Light Rail and Heavy Rail route names.
2. Display the route with the most stops, and that number of stops.
3. Display the route with the fewest stops, and that number of stops.
4. Display all the stations which serve multiple routes.
5. Display a sample route with transfers between two stations. 
Additionally, you can exit the program with option `6`.
You can refresh the data without restarting the program with option `0`.

Information about the subway routes and stops is retrieved from the MBTA's APIs (https://api-v3.mbta.com). 

#### Notes
By default, this program only assesses "Light Rail" (trolleys) and "Heavy Rail" (subways) systems.
This is achieved by applying a filter of types to the `/routes` endpoint when called.
This was chosen as the default (as opposed to getting all routes and filtering) to reduce the size of the server response
(in the case of a slow connection). This behavior can be altered by changing the route types filtered.
Furthermore all route types can be selected by passing no filter argument.