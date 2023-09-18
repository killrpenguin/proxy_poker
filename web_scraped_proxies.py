import requests
import random
from bs4 import BeautifulSoup


class gather_proxies:
    def __init__(self, proxy):
        self.user_agent = self.get_user_agents()
        self.proxy = self.get_big_proxys()
        # A method for instantiating the selenium webdriver for asycronious scraping.
        self.sel_driver = self.sel_driver(proxy=self.proxy, user_agent=self.user_agent)
        self.all_proxies = ()

    def get_user_agents(self):
        status_codes = [200]
        with requests.get("https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt") as git_page:
            try:
                if git_page.status_code in status_codes:
                    html = BeautifulSoup(git_page.text, 'html.parser')
                    user_agent_list = html.text.strip().split('\n')
                    return user_agent_list.pop(random.randint(0, len(user_agent_list)))
            except Exception as e:
                print(f"{git_page.status_code} {e}")

    def get_big_proxys(self):
        status_codes = [200]
        with requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt") as big_proxies:
            try:
                if big_proxies.status_code in status_codes:
                    html = BeautifulSoup(big_proxies.text, 'html.parser')
                    proxy_list = html.text.strip().split('\n')
                    return proxy_list.pop(random.randint(0, len(proxy_list)))
            except Exception as e:
                print(f"{big_proxies.status_code} {e}")

    def sel_driver(self, proxy, user_agent):
        return self.sel_driver
        pass