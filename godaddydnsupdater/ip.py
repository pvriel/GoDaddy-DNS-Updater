from logging import getLogger, Logger
from typing import Set
from os import environ
from json import JSONDecoder
from ipaddress import IPv4Address, IPv6Address, ip_address
from requests import get

logger: Logger = getLogger("godaddy_dns_updater.ip")
logger.setLevel(environ.get('LOG_LEVEL', 'INFO'))

current_ip_sources: Set[str] = {"https://api.ipify.org?format=json", "https://api64.ipify.org?format=json"}


def fetch_current_addresses() -> Set[IPv4Address | IPv6Address]:
    logger.info("Fetching current IP addresses...")
    return_value: Set[IPv4Address | IPv6Address] = set()

    for source in current_ip_sources:
        try:
            response = get(source)
            response_json = JSONDecoder().decode(response.text)
            return_value.add(ip_address(response_json["ip"]))
            logger.debug(f"Found IP address ({response_json['ip']}) from source ({source}).")
        except BaseException as e:
            logger.warning(f"Failed to fetch IP address from source ({source}) (reason: {e}); continuing...")

    logger.info(f"Found {len(return_value)} current IP address(es): ({set(str(address) for address in return_value)}).")
    return return_value
