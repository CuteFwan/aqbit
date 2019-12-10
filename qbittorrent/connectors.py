from .errors import TorrentHashNotFound, TorrentNotValid, HttpException
import aiohttp
import asyncio
import json

class AConnector:

    def __init__(self, *, base, session = None, loop = None):
        self.base = base
        self.loop = loop or asyncio.get_event_loop()
        self.session = session

    async def request(self, method, path : str, *, payload = None):
        url = self.base + path
        retries = 5

        while retries:
            async with self.session.request(method, url, data=payload) as r:
                data = await r.text(encoding='utf-8')
                if r.headers.get('Content-Type', None) == 'application/json':
                    data = json.loads(data)
                if r.status == 200:
                    """Everything is fine?"""
                    return data
                elif r.status == 403:
                    """Login has probably been invalidated. retry."""
                    await self.login(self.credentials['username'], self.credentials['password'])
                elif r.status == 400:
                    retries -= 1
                    print(f'Bad Http request, retrying {retries}')
                    await asyncio.sleep(1)
                elif r.status == 404:
                    raise TorrentHashNotFound(r, data)
                elif r.status == 415:
                    raise TorrentNotValid(r, data)
                else:
                    return r.status, data
        raise HttpException(r, data)

    async def login(self, username : str, password : str):
        """
        Attempt to log into the web api using a username and password.

        Parameters
        ----------
        username: str
            The username to log into the web api
        password: str
            The password to log into the web api

        """
        if not self.session:
            self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True))
        payload = {
            'username' : username,
            'password' : password
            }
        self.credentials = payload
        return await self.request('POST', '/auth/login', payload=self.credentials)

    async def logout(self):
        """Attempt to log out of the webapi"""

        return await self.request('POST', '/auth/logout')

        await self.session.close()


import requests

class RConnector:

    def __init__(self, *, base, session = None):
        self.base = base
        self.session = session or requests.Session()

    def request(self, method, path : str, *, payload = None):
        url = self.base + path
        retries = 5

        while retries:
            r = self.session.request(method, url, data=payload)
            if r.status_code == 200:
                data = r.text
            if r.headers.get('Content-Type', None) == 'application/json':
                return json.loads(data)
            return data
    def login(self, username : str, password : str):
        if not self.session:
            self.session = requests.Session()
        payload = {
            'username' : username,
            'password' : password
            }
        self.credentials = payload
        return self.request('POST', '/auth/login', payload=self.credentials)
    def logout(self):
        self.session.close()