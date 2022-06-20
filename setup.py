from setuptools import setup
from pathlib import Path
import re

version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open("bnmp_scraper/settings.py", "r") as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        VERSION = match.group(1)
    else:
        raise RuntimeError("No version number found!")


setup(
    name='bnmp_scraper',
    version=VERSION,

    url='https://github.com/olucaslopes/BNMP-Scraper',
    author='Lucas Lopes',
    author_email='lucaslopesamorim@gmail.com',
    description='Navega pela API do Portal BNMP coletando dados',
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",

    packages=['bnmp_scraper'],
    install_requires=[
        'requests',
        'tqdm'
    ],
)
