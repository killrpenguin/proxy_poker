from web_scraped_proxies import Sel_Driver, Master_Proxy_List

proxy = "http://43.157.8.79:8888"
test = Master_Proxy_List(proxy=proxy)
test.populate_proxy_list()
for i in test.all_proxies:
    print(i.address)