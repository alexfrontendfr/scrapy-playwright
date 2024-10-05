import requests
from bs4 import BeautifulSoup
import random

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.update_proxy_list()

    def update_proxy_list(self):
        try:
            response = requests.get('https://free-proxy-list.net/')
            soup = BeautifulSoup(response.text, 'html.parser')
            proxy_list = soup.find('table', id='proxylisttable').find_all('tr')[1:]
            
            self.proxies = []
            for row in proxy_list:
                columns = row.find_all('td')
                if columns[6].text.strip() == 'yes':  # Check if it's an HTTPS proxy
                    ip = columns[0].text.strip()
                    port = columns[1].text.strip()
                    self.proxies.append(f'http://{ip}:{port}')
            
            print(f"Updated proxy list with {len(self.proxies)} proxies")
        except Exception as e:
            print(f"Error updating proxy list: {e}")

    def get_random_proxy(self):
        if not self.proxies:
            self.update_proxy_list()
        return random.choice(self.proxies) if self.proxies else None

proxy_manager = ProxyManager()

