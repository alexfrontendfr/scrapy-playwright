import requests
import logging
from requests.exceptions import RequestException
from typing import List, Optional
import time
import stem
from stem.control import Controller
from stem import Signal
import socks
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self):
        self.proxies: List[str] = []
        self.last_fetch_time: float = 0
        self.cache_duration: int = 3600  # Cache proxies for 1 hour

    def refresh_proxies(self):
        self._fetch_proxies()
        self.last_fetch_time = time.time()    

    def get_proxies(self) -> List[str]:
        if self._should_refresh_cache():
            self._fetch_proxies()
        return self.proxies

    def _should_refresh_cache(self) -> bool:
        return time.time() - self.last_fetch_time > self.cache_duration

    def _fetch_proxies(self) -> None:
        url = 'https://www.proxy-list.download/api/v1/get?type=https'  # Free proxy API
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.proxies = [proxy for proxy in response.text.split('\r\n') if proxy]
            self.last_fetch_time = time.time()
            logger.info(f"Successfully fetched {len(self.proxies)} proxies")
        except RequestException as e:
            logger.error(f"Error fetching proxies: {e}")
            if not self.proxies:
                logger.warning("No cached proxies available. Using direct connection.")

    def get_random_proxy(self) -> Optional[str]:
        proxies = self.get_proxies()
        return proxies[int(time.time()) % len(proxies)] if proxies else None

class TorManager:
    def __init__(self, tor_port: int = 9051, tor_password: Optional[str] = None):
        self.tor_port = tor_port
        self.tor_password = tor_password
        self.socks_port = 9050
        self.controller = None

    def start(self):
        try:
            self.controller = Controller.from_port(port=self.tor_port)
            if self.tor_password:
                self.controller.authenticate(password=self.tor_password)
            else:
                self.controller.authenticate()
            logger.info("Successfully connected to Tor controller")
        except stem.SocketError as e:
            logger.error(f"Error connecting to Tor controller: {e}")
        except stem.ControllerError as e:
            logger.error(f"Error authenticating with Tor controller: {e}")

    def renew_tor_ip(self) -> None:
        if not self.controller:
            self.start()
        try:
            self.controller.signal(Signal.NEWNYM)
            logger.info("Successfully renewed Tor IP address")
        except Exception as e:
            logger.error(f"Error renewing Tor IP: {e}")

    def get_tor_session(self):
        session = requests.session()
        session.proxies = {'http':  f'socks5://localhost:{self.socks_port}',
                           'https': f'socks5://localhost:{self.socks_port}'}
        return session

    def stop(self):
        if self.controller:
            self.controller.close()
            logger.info("Tor controller closed")

def get_tor_proxy() -> str:
    return f'socks5://127.0.0.1:9050'

def set_tor_proxy():
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket

# Initialize the ProxyManager
proxy_manager = ProxyManager()

# Initialize the TorManager
tor_manager = TorManager()

# Function to get proxies (for compatibility with keyword_spider.py)
def get_proxies() -> List[str]:
    return proxy_manager.get_proxies()