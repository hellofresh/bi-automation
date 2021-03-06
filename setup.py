from setuptools import setup, find_packages

NAME = "biautomation"
VERSION = "1.1.0"

REQUIRES = [
    'boto'
]

setup(
    name=NAME,
    version=VERSION,
    description="BI Automation",
    author_email="tm@hellofresh.com",
    keywords=["HelloFresh", "BI", "Automation"],
    install_requires=REQUIRES,
    packages=find_packages()
)
