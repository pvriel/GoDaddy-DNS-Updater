from ipaddress import IPv4Address, IPv6Address, ip_address
from logging import Logger, getLogger
from os import environ
from socket import gethostbyname_ex
from typing import Set

logger: Logger = getLogger("godaddy_dns_updater.dns")
logger.setLevel(environ.get('LOG_LEVEL', 'INFO'))


def get_ip_addresses_for_host(name: str) -> Set[IPv4Address | IPv6Address]:
    logger.debug(f"Fetching IP addresses for host ({name})...")
    return_value: Set[IPv4Address | IPv6Address] = set()
    for ip_address_str in gethostbyname_ex(name)[2]:
        try:
            return_value.add(ip_address(ip_address_str))
            logger.debug(f"Found IP address ({ip_address_str}) for host ({name}).")
        except BaseException as e:
            logger.warning(f"Failed to fetch IP address ({ip_address_str}) for host ({name}) (reason: {e}); continuing...")

    logger.debug(f"Found {len(return_value)} IP address(es) for host ({name}): ({return_value}).")
    return return_value
