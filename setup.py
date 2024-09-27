
from setuptools import setup, find_packages

setup(
    name="scrapy_playwright",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "scrapy>=2.5.1",
        "playwright>=1.12.0",
        "beautifulsoup4>=4.9.3",
        "requests>=2.25.1",
        "lxml>=4.6.3",
    ],
    author="Your Name",
    author_email="you@example.com",
    description="A web scraper using Scrapy and Playwright",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/scrapy-playwright",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
