from ipaddress import IPv4Address, IPv6Address
from logging import Logger, getLogger, StreamHandler
from os import environ

from ratelimit import limits
from typing import TypeVar, Callable, Set, Any, Dict, List, Optional
from godaddypy import Client, Account

logger: Logger = getLogger("godaddy_dns_updater.godaddy")
logger.setLevel(environ.get('LOG_LEVEL', 'INFO'))

class GoDaddyAPIHandler:

    T: TypeVar = TypeVar('T')
    ONE_MINUTE: int = 60
    MAX_GODADDY_API_CALLS_PER_MINUTE: int = 60

    def __init__(self, api_key: str, api_secret: str) -> None:
        super().__init__()

        account: Account = Account(api_key=api_key, api_secret=api_secret)
        self.__client__: Client = Client(account=account)

    def update_domain(self, domain_name: str, sub_domains: Set[str], ip_addresses: Set[IPv4Address | IPv6Address],
                      ttl: int = 1200) -> None:
        logger.info(f"managing domain ({domain_name})...")
        old_records: List[Dict[str, Any]] = self.get_records(domain_name)
        for sub_domain in sub_domains:
            self.__update_subdomain__(old_records, domain_name, sub_domain, ip_addresses, ttl)
        logger.info(f"Finished managing domain ({domain_name}).")

    def get_records(self, domain_name: str) -> List[Dict[str, Any]]:
        return GoDaddyAPIHandler.__apply_godaddy_rate_limitation__(
            f=lambda: self.__client__.get_records(domain=domain_name))

    def __update_subdomain__(self, old_records: List[Dict[str, Any]], domain_name: str, sub_domain: str,
                             ip_addresses: Set[IPv4Address | IPv6Address], ttl: int) -> None:
        # Making the strong assumption here that domains only need to be created / updated, and not removed!
        logger.info(f"Managing subdomain ({sub_domain}.{domain_name})...")
        for ip_address in ip_addresses:
            self.__update_subdomain_ip__(old_records, domain_name, sub_domain, ip_address, ttl)

        logger.debug(f"Finished managing subdomain ({sub_domain}.{domain_name}).")

    def __update_subdomain_ip__(self, old_records: List[Dict[str, Any]], domain_name: str, sub_domain: str,
                                ip_address: IPv4Address | IPv6Address, ttl: int) -> None:
        record_type: str = "A" if isinstance(ip_address, IPv4Address) else "AAAA"
        optional_old_record = self.__pop_old_subdomain_info_from_old_records__(sub_domain, old_records, record_type)
        should_be_updated: bool = (optional_old_record is None or optional_old_record["data"] != str(ip_address) or
                                   optional_old_record["ttl"] != ttl)
        if not should_be_updated:
            return

        new_record: Dict[str, Any] = {"data": str(ip_address), "ttl": ttl, "type": record_type, "name": sub_domain}
        if not optional_old_record:
            GoDaddyAPIHandler.__apply_godaddy_rate_limitation__(
                f=lambda: self.__client__.add_record(domain=domain_name, record=new_record))
            logger.debug(f"Added new record for subdomain ({sub_domain}.{domain_name}): ({new_record})")
        else:
            GoDaddyAPIHandler.__apply_godaddy_rate_limitation__(
                f=lambda: self.__client__.update_record(domain=domain_name, record=new_record))
            logger.debug(f"Updated record for subdomain ({sub_domain}.{domain_name}): ({optional_old_record}) -> "
                         f"({new_record})")
    @staticmethod
    def __pop_old_subdomain_info_from_old_records__(sub_domain: str, old_records: List[Dict[str, Any]], record_type: str) -> Optional[Dict[str, Any]]:
        for i in range(len(old_records)):
            if old_records[i]["name"] == sub_domain and old_records[i]["type"] == record_type:
                return old_records.pop(i)

        return None

    @staticmethod
    @limits(calls=MAX_GODADDY_API_CALLS_PER_MINUTE, period=ONE_MINUTE)
    def __apply_godaddy_rate_limitation__(f: Callable[[], T]) -> T:
        return f()
