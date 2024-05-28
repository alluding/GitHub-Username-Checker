from typing import (
    Dict, 
    Union,
    Optional,
)
import requests
from requests.adapters import HTTPAdapter
from requests.sessions import Session

class _Session(Session):
    def __init__(self, use_proxies: bool = False) -> None:
        super().__init__()
        
        if use_proxies:
            self._configure_proxies()

    def _configure_proxies(self) -> None:
        for prefix in ['http://', 'https://']:
            self.mount(prefix, HTTPAdapter(max_retries=3))

    def check_username(self, username: str) -> Union[bool, str, None]:
        codes = {self.get(url.format(username)).status_code for url in ['https://github.com/{}', 'https://api.github.com/users/{}']}
        
        return (
            True if 404 in codes and all(code == 404 for code in codes) else
            False if 200 in codes else
            "Rate limited!" if 403 in codes else
            None
        )

    def proxy_check(self, username: str, proxy: Optional[ProxyConfig]) -> Union[bool, str, None]:
        if not proxy:
            raise ValueError("Proxy configuration is required for proxy support.")

        adapter = self.get_adapter("http://")
        if not isinstance(adapter, HTTPAdapter):
            raise ValueError("Proxy support requires the HTTPAdapter.")
        
        manager = getattr(adapter, 'proxy_manager', None)
        if manager:
            setattr(adapter, 'proxy_manager', self.adapters['http://'].proxy_manager)

        codes = {self.get(url.format(username), proxies=proxy).status_code for url in ['https://github.com/{}', 'https://api.github.com/users/{}']}
        
        return (
            True if 404 in codes and all(code == 404 for code in codes) else
            False if 200 in codes else
            "Rate limited!" if 403 in codes else
            None
        )

    def set_request_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)
