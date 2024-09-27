import requests
import logging
from requests.exceptions import RequestException
from typing import List, Optional
import time
import stem
from stem.control import Controller
from stem import Signal

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self):
        self.proxies: List[str] = []
        self.last_fetch_time: float = 0
        self.cache_duration: int = 3600  # Cache proxies for 1 hour

    def get_proxies(self) -> List[str]:
        if self._should_refresh_cache():
            self._fetch_proxies()
        return self.proxies

    def _should_refresh_cache(self) -> bool:
        return time.time() - self.last_fetch_time > self.cache_duration

    def _fetch_proxies(self) -> None:
        url = 'https://www.proxy-list.download/api/v1/get?type=http'  # Free proxy API
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

    def renew_tor_ip(self) -> None:
        try:
            with Controller.from_port(port=self.tor_port) as controller:
                if self.tor_password:
                    controller.authenticate(password=self.tor_password)
                else:
                    controller.authenticate()
                controller.signal(Signal.NEWNYM)
                logger.info("Successfully renewed Tor IP address")
        except stem.SocketError as e:
            logger.error(f"Error connecting to Tor controller: {e}")
        except stem.ControllerError as e:
            logger.error(f"Error authenticating with Tor controller: {e}")

def get_tor_proxy() -> str:
    return 'socks5://127.0.0.1:9050'

# Initialize the ProxyManager
proxy_manager = ProxyManager()

# Initialize the TorManager
tor_manager = TorManager()