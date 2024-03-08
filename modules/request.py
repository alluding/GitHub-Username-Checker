from typing import Dict, Union, Optional, TYPE_CHECKING

import requests
from requests.adapters import HTTPAdapter
from requests.sessions import Session

if TYPE_CHECKING:
    from requests.sessions import Session

class _Session(Session):
    def __init__(self, use_proxies: bool = False) -> None:
        super().__init__()
        self.configure_proxies(use_proxies)

    def configure_proxies(self, use_proxies: bool) -> None:
        if use_proxies:
            for prefix in ['http://', 'https://']:
                self.mount(prefix, HTTPAdapter(max_retries=3))

    def check_username(self, username: str) -> Union[bool, str, None]:
        html, api = (self.get(url.format(username)).status_code for url in ['https://github.com/{}', 'https://api.github.com/users/{}'])
        return True if html == 404 and (api := self.get(f'https://api.github.com/users/{username}').status_code) == 404 else False if html == 200 else "Rate limited!" if html == 403 else None

    def proxy_check(self, username: str, proxy: Optional[Dict[str, str]]) -> Union[bool, str, None]:
        if not proxy:
            raise ValueError("Proxy configuration is required for proxy support.")

        adapter = self.get_adapter("http://")
        if not isinstance(adapter, HTTPAdapter):
            raise ValueError("Proxy support requires the HTTPAdapter.")

        setattr(adapter, 'proxy_manager', self.adapters['http://'].proxy_manager)

        html, api = (self.get(url.format(username), proxies=proxy).status_code for url in ['https://github.com/{}', 'https://api.github.com/users/{}'])
        return True if html == 404 and (api := self.get(f'https://api.github.com/users/{username}', proxies=proxy).status_code) == 404 else False if html == 200 else "Rate limited!" if html == 403 else None

    def set_request_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)
