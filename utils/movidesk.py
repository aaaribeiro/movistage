# built-in libraries
import logging # libvrary for logging
import logging.config # logging config file

# third-party libraries
import requests

# personal modules 
# import utils

# configuring logging hanlder for script
# logging.config.fileConfig("logging.config")
# logger = logging.getLogger(__name__)
# logger.debug(f"{__name__} log done, starting the application")

########################### CONSTANTS #############################
URL = "https://api.movidesk.com/public/v1"
TOKEN = "27d95ace-819c-43d8-bb93-5c39dbf5edbd"
###################################################################

# @utils.debug
def get_ticket(id: int, url: str=URL, token: str=TOKEN):
    params = {"token": token, "id": {id}}
    try:
        ticket = requests.get(f"{url}/tickets", params=params)
        # logger.debug(f"{ticket.url}")
        ticket.raise_for_status()
    except requests.HTTPError as err:
        # error_code = err.response.status_code
        # endpoint = err.response.url
        # message = "Ticket not found"
        # logger.error(f"{error_code} {message} {endpoint}")
        print("movidesk ticket not found")
        exit(1)
    else:
        return ticket.json()


def get_organization(id: str, url: str=URL, token: str=TOKEN):
    params = {"token": token, "id": {id}}
    try:
        organization = requests.get(f"{url}/persons", params=params)
        # logger.debug(f"{ticket.url}")
        organization.raise_for_status()
    except requests.HTTPError as err:
        # error_code = err.response.status_code
        # endpoint = err.response.url
        # message = "Ticket not found"
        # logger.error(f"{error_code} {message} {endpoint}")
        print("movidesk organization not found")
        exit(1)
    else:
        return organization.json()


# Class

