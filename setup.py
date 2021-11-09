from setuptools import setup
from pathlib import Path


setup(
    name='bnmp_scraper',
    version='0.0.1',

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
