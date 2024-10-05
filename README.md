# Matrix Web Scraper Installation and Running Guide

## Prerequisites

- Debian-based system (e.g., Debian 10 or Ubuntu 20.04)
- sudo access

## Installation Steps

1. Update system and install dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-venv tor proxychains4 iptables-persistent dnscrypt-proxy redis-server libpq-dev build-essential libssl-dev libffi-dev python3-dev postgresql postgresql-contrib
```

2. Clone the repository:
   git clone https://github.com/alexfrontendfr/scrapy-playwright.git
   cd scrapy-playwright

3. Set up virtual environment:

   python3 -m venv venv
   source venv/bin/activate

4. Install project dependencies:

   pip install --upgrade pip
   pip install -r requirements.txt
   playwright install

5. Configure TOR

   sudo nano /etc/tor/torrc

6. Add or uncomment the following lines:

SocksPort 9050
ControlPort 9051
HashedControlPassword 16:01234567890ABCDEF01234567890ABCDEF01234567890ABCDEF01234567

Generate a hashed password:
tor --hash-password "your_password_here"

Replace the HashedControlPassword line with the generated hash.
Restart TOR:
sudo systemctl restart tor

6. Configure ProxyChains:
   sudo nano /etc/proxychains4.conf

7. Add the following line at the end of the file:
   socks5 127.0.0.1 9050

8. Configure firewall:

   Create configure_firewall.sh in the project root and add the content from step 5 in the previous message.
   Apply firewall rules:
   sudo bash configure_firewall.sh

9. Configure DNSCrypt-proxy:

   sudo nano /etc/dnscrypt-proxy/dnscrypt-proxy.toml

Update the settings as mentioned in step 6 of the previous message.
Restart DNSCrypt-proxy:

sudo systemctl restart dnscrypt-proxy

Update the settings as mentioned in step 6 of the previous message.
Restart DNSCrypt-proxy:
sudo systemctl restart dnscrypt-proxy

Update resolv.conf:
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf
echo "options edns0" | sudo tee -a /etc/resolv.conf

9. Set up PostgreSQL:
   sudo -u postgres psql -c "CREATE DATABASE matrix_scraper;"
   sudo -u postgres psql -c "CREATE USER scraper_user WITH PASSWORD 'your_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE matrix_scraper TO scraper_user;"

10. Configure environment variables:

Create a .env file in the project root:

11. Initialize the database:

python

12. In the Python interpreter:

from scraper_bot.models import Base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)

exit()

Running the Project

1. Start Redis server:
   sudo systemctl start redis-server

2. Start Celery worker:

   celery -A scraper_bot.tasks worker --loglevel=info

3. Run the Flask application:

   python scraper_bot/app.py

4. Access the web interface:

Open a web browser and navigate to http://localhost:5000
Usage

Enter your search query in the provided field.
Select the desired search engines (Google, Bing, DuckDuckGo, Onion).
Set the result limit.
Choose whether to use TOR for anonymous scraping.
Click "Start Search" and wait for the results.

Maintenance

To clear the cache: Send a POST request to http://localhost:5000/clear_cache
To renew the TOR IP: Send a POST request to http://localhost:5000/renew_tor_ip

Troubleshooting

If you encounter any issues with TOR, try restarting the service

sudo systemctl restart tor

If the database connection fails, ensure PostgreSQL is running:

sudo systemctl status postgresql

For any other issues, check the scraper.log file for error messages.
