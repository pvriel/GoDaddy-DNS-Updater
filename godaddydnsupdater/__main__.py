from ipaddress import IPv4Address, IPv6Address
from logging import StreamHandler, getLogger, Logger, Formatter
from os import environ
from time import sleep
from typing import Set

from godaddydnsupdater.dns import get_ip_addresses_for_host
from godaddydnsupdater.godaddy import GoDaddyAPIHandler
from godaddydnsupdater.ip import fetch_current_addresses

logger: Logger = getLogger("godaddy_dns_updater")
logger.setLevel(environ.get('LOG_LEVEL', 'INFO'))
handler: StreamHandler = StreamHandler()
formatter: Formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_which_subdomains_might_need_updates(domain: str, sub_domains: Set[str],
                                              current_ip_addresses: Set[IPv4Address | IPv6Address]) -> Set[str]:
    logger.info("Checking subdomains...")
    return_value: Set[str] = set()
    for sub_domain in sub_domains:
        ip_addresses_sub_domain: Set[IPv4Address | IPv6Address] = get_ip_addresses_for_host(f"{sub_domain}.{domain}")
        if ip_addresses_sub_domain != current_ip_addresses:
            return_value.add(sub_domain)

    logger.info(f"Found {len(return_value)} subdomain(s): ({return_value}).")
    return return_value


def main():
    godaddy_api_handler: GoDaddyAPIHandler = GoDaddyAPIHandler(environ['GODADDY_API_KEY'], environ['GODADDY_API_SECRET'])
    domain: str = environ['DOMAIN']
    ttl: int = int(environ.get('TTL', '1200'))
    timeout: int = int(environ.get('TIMEOUT', '300'))
    logger.info(f"Updating domain ({domain})...")
    sub_domains: Set[str] = set(environ['SUBDOMAINS'].split(','))

    while True:
        current_ip_addresses: Set[IPv4Address | IPv6Address] = fetch_current_addresses()
        try:
            godaddy_api_handler.update_domain(domain, sub_domains, current_ip_addresses, ttl)
        except BaseException as e:
            logger.error(f"Failed to update domain ({domain}) (reason: {e}).")
        logger.info(f"Iteration done. Next iteration in {timeout} second(s)...")
        sleep(timeout)


if __name__ == "__main__":
    main()
