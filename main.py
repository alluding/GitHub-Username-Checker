import json
from typing import Dict, List, Union
from colorama import Fore, Style

from modules.process import process_usernames
from modules.request import _Session


class UsernameChecker:
    def __init__(self, _config: str = "./data/config.json"):
        self.config: Dict[str, Union[bool, Dict[str, str]]] = json.load(open(_config))
        self.use_proxies: bool = self.config.get("use_proxies", True)

        self.session: _Session = _Session(use_proxies=self.use_proxies)
        self.proxy: Dict[str, str] = self.config.get("proxy", {}) if self.use_proxies else {}

        self.usernames: List[str] = process_usernames(self.config["usernames"])
        self.usernames_to_check: List[str] = open(self.config["usernames"]).read().splitlines()

    def check_usernames(self) -> List[str]:
        return [self.format_output(username, self.check(username)) for username in self.usernames_to_check]

    def check(self, username: str) -> bool:
        result = self.session.proxy_check(
            username, self.proxy) if self.use_proxies else self.session.check_user(username)
        print(f"{self._format(username, result)}\n", end='', flush=True)

    def _format(self, username: str, result: bool) -> str:
        status: str = "available" if result else "taken"
        color: str = Fore.GREEN if result else Fore.RED
        return f"[{color}{username}{Style.RESET_ALL}] - {status}"

if __name__ == "__main__":
    checker: UsernameChecker = UsernameChecker()
    checker.check_usernames()
