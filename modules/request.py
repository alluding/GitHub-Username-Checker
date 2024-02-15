from typing import Dict

import requests

class _Session(requests.Session):
    def __init__(self, use_proxies: bool = False):
        super().__init__()
        self.configure_proxies(use_proxies)

    def configure_proxies(self, use_proxies: bool):
        if use_proxies:
            self.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
            self.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))

    def check_username(self, username: str) -> bool:
        return self.get(f'https://api.github.com/users/{username}').status_code == 404

    def proxy_check(self, username: str, proxy: Dict[str, str]) -> bool:
        if not proxy:
            raise ValueError(
                "Proxy configuration is required for proxy support.")

        adapter = self.get_adapter("http://")
        if not isinstance(adapter, requests.adapters.HTTPAdapter):
            raise ValueError("Proxy support requires the HTTPAdapter.")

        setattr(adapter, 'proxy_manager',
                self.adapters['http://'].proxy_manager)

        return self.get(f'https://api.github.com/users/{username}', proxies=proxy).status_code == 404

    def set_request_headers(self, headers: Dict[str, str]):
        for key, value in headers.items():
            setattr(self.headers, key, value)
