from setuptools import setup, find_packages
from qbittorrent import __version__ as version, __title__ as name, __author__ as author, __license__ as license


setup(
    name=name,
    version=version,
    author=author,
    url="https://github.com/CuteFwan/aqbit",
    license="MIT",
    description="Async qbittorrent webapi wrapper.",
    keywords="aqbit",
    packages=find_packages()
)