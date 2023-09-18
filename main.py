import requests
from bs4 import BeautifulSoup
import random


user_agents = requests.get("https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt")
soup = BeautifulSoup(user_agents.text, 'html.parser')
user_agent_list = soup.text.strip().split('\n')
test = user_agent_list.pop(random.randint(0, len(user_agent_list)))
test1 = user_agent_list.pop(random.randint(0, len(user_agent_list)))
test2 = user_agent_list.pop(random.randint(0, len(user_agent_list)))
print(f"{test}\n{test1}\n{test2}")
