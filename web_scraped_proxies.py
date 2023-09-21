import requests
import random
import selenium
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from dataclasses import dataclass, field
from selenium.webdriver import EdgeOptions


# This data class will be used to store all proxies gathered for Master_Proxy_List

@dataclass(kw_only=True)
class proxy_obj:
    # IP Address including port number.
    address: str = field(default=str)
    # possile protocol types include sock5, sock4, HTTPS, HTTP
    protocol: str = field(default=str)
    # This value is supplied from some scraped web pages but is updated periodically with a method.
    latency: str = field(default=str)


# This object will be used to create asynchronous web drivers with selenium.
class Sel_Driver(selenium.webdriver):
    def __init__(self, proxy):
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument('headless')
        edge_options.add_argument('disable-gpu')
        self.proxy = proxy
        self.user_agent = self.get_user_agents()
        self.driver = selenium.webdriver.Edge(options=edge_options)


    def get_user_agents(self):
        status_codes = [200]
        with requests.get(
                "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw"
                "/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt") as git_page:
            try:
                if git_page.status_code in status_codes:
                    html = BeautifulSoup(git_page.text, 'html.parser')
                    user_agent_list = html.text.strip().split('\n')
                    return user_agent_list.pop(random.randint(0, len(user_agent_list)))
            except Exception as e:
                print(f"{git_page.status_code} {e}")


class Master_Proxy_List:
    def __init__(self, proxy):
        self.driver = Sel_Driver(proxy)
        self.all_proxies = []

    def populate_proxy_list(self):
        self.get_fivek_list()
        self.get_site_proxyscraper()

    def get_fivek_list(self):
        status_codes = [200]
        with requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt") as big_proxies:
            try:
                if big_proxies.status_code in status_codes:
                    html = BeautifulSoup(big_proxies.text, 'html.parser')
                    self.all_proxies = html.text.strip().split('\n')
                    self.all_proxies = [proxy_obj(address=proxy) for proxy in self.all_proxies]
                    return self.all_proxies
            except Exception as e:
                print(f"{big_proxies.status_code} {e}")

    def get_site_proxyscraper(self):
        xpath = '//*[@id="proxytable"]/tr'
        page = "https://proxyscrape.com/free-proxy-list-f"
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(page)
        if self.driver.page_source > 0:
            try:
                proxy_table = wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath)))
                proxy_table = [proxy.text for proxy in proxy_table]
                for i in proxy_table:
                    address = re.search("^\d.+?\s\d.+?\s", i)
                    protocol = re.search("H.+?\s|So.+?\d\s", i)
                    latency = re.search("\d{2,4}ms", i)
                    self.all_proxies.append(proxy_obj(address=address.group().replace(" ", ":", 1).strip(),
                                           protocol=protocol.group().strip(),
                                           latency=latency.group().strip()
                                           ))
                return self.all_proxies
            except Exception as e:
                print(f"{e}")