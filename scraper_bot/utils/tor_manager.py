from stem import Signal
from stem.control import Controller
from scraper_bot import settings

def renew_tor_ip():
    with Controller.from_port(port=settings.TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=settings.TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)
        print("New Tor IP requested")

def get_tor_proxy():
    return settings.TOR_PROXY