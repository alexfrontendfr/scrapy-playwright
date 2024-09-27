import os

search_terms = ["gay community", "LGBT tech", "tech startups", "cybersecurity", "open-source software"]

for term in search_terms:
    formatted_term = term.replace(' ', '+')
    os.system(f'scrapy crawl keyword_spider -a keyword="{formatted_term}"')
