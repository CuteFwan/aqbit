import aiohttp
import asyncio
import json

from .errors import TorrentNotValid, TorrentHashNotFound, FailedLogin, HttpException

class QBittorrentClient:
    """
    QBittorent client

    """
    def __init__(self, base, *, connector):
        self.connector = connector
        self.base = base



    def get_application_version(self):
        """
        Grab the application version of QBittorent.

        Returns
        -------
        str
        """
        return self.connector.request('GET', '/app/version')

    def get_api_version(self):
        """
        Grab the api version.

        Returns
        -------
        str

        """
        return self.connector.request('GET', '/app/webapiVersion')

    def get_log(self, **kwargs):
        """
        Grabs the log.

        Parameters
        ----------
        normal: bool, optional
            Include normal messages
        info: bool, optional
            Include info messages
        warning: bool, optional
            Include warning messages
        critical: bool, optional
            Include critical messages
        last_known_id: int, optional
            Exclude messages with "message id" <= last_known_id

        Returns
        -------
        dict
        """

        payload = {
            'normal' : kwargs.get('normal', True),
            'info' : kwargs.get('info', True),
            'warning' : kwargs.get('warning', True),
            'critical' : kwargs.get('critical', True),
            'last_known_id' : kwargs.get('last_known_id', -1)

        }

        return self.connector.request('GET', '/log/main', payload=payload)

    def get_torrents(self, **kwargs):
        """
        Gets the list of torrents.

        Parameters
        ----------
        filter: str, optional
            Filter torrent list.
            Allowed filters: all, downloading, completed, paused, active, inactive, resumed
        category: str, optional
            Get torrents with the given category
            Empty string means "without category"
            No "category" parameter means "any category"
        sort: str, optional
            Sort torrents by given key.
        reverse: bool, optional
            Enable reverse sorting.
        limit: int, optional
            Limit the number of torrents returned
        offset: int, optional
            Set offset (if less than 0, offset from end)
        hashes: list or str, optional
            Filter by hashes.
        
        Returns
        -------
        dict

        Property        Type    Description
        hash            string  Torrent hash
        name            string  Torrent name
        size            integer Total size (bytes) of files selected for download
        progress        float   Torrent progress (percentage/100)
        dlspeed         integer Torrent download speed (bytes/s)
        upspeed         integer Torrent upload speed (bytes/s)
        priority        integer Torrent priority. Returns -1 if queuing is disabled or torrent is in seed mode
        num_seeds       integer Number of seeds connected to
        num_complete    integer Number of seeds in the swarm
        num_leechs      integer Number of leechers connected to
        num_incomplete  integer Number of leechers in the swarm
        ratio           float   Torrent share ratio. Max ratio value: 9999.
        eta             integer Torrent ETA (seconds)
        state           string  Torrent state. See table here below for the possible values
        seq_dl          bool    True if sequential download is enabled
        f_l_piece_prio  bool    True if first last piece are prioritized
        category        string  Category of the torrent
        super_seeding   bool    True if super seeding is enabled
        force_start     bool    True if force start is enabled for this torrent

        Possible values of state:
        
        Value               Description
        error               Some error occurred, applies to paused torrents
        missingFiles        Torrent data files is missing
        uploading           Torrent is being seeded and data is being transferred
        pausedUP            Torrent is paused and has finished downloading
        queuedUP            Queuing is enabled and torrent is queued for upload
        stalledUP           Torrent is being seeded, but no connection were made
        checkingUP          Torrent has finished downloading and is being checked
        forcedUP            Torrent is forced to uploading and ignore queue limit
        allocating          Torrent is allocating disk space for download
        downloading         Torrent is being downloaded and data is being transferred
        metaDL              Torrent has just started downloading and is fetching metadata
        pausedDL            Torrent is paused and has NOT finished downloading
        queuedDL            Queuing is enabled and torrent is queued for download
        stalledDL           Torrent is being downloaded, but no connection were made
        checkingDL          Same as checkingUP, but torrent has NOT finished downloading
        forceDL             Torrent is forced to downloading to ignore queue limit
        checkingResumeData  Checking resume data on qBt startup
        moving              Torrent is moving to another location
        unknown             Unknown status

        """
        defaults = {
            'filter' : None,
            'category' : None,
            'sort' : None,
            'reverse' : None,
            'limit' : None,
            'offset' : None,
            'hashes' : None
        }
        payload = { k : kwargs.get(k, v) for k, v in defaults.items() if v or kwargs.get(k)}
        hashes = kwargs.get('hashes')
        if hashes:
            payload['hashes'] = '|'.join(hashes) if isinstance(hashes, list) else hashes
        print(payload)
        return self.connector.request('POST', '/torrents/info', payload=payload)


    def add_torrent(self, link : str, path : str):
        """
        Adds a single torrent.

        Parameters
        ----------
        link: str
            Can be a link to a torrent file or a magnet link.
        path: str
            The folder to download to.
        """
        payload = {
            'urls' : link,
            'savepath' : path
        }
        return self.connector.request('POST', '/torrents/add', payload=payload)

    def add_multi_torrents(self, links : list, path : str):

        """
        Adds multiple torrents.

        Parameters
        ----------
        links: list
            A list of urls. Can be to torrent files or magnet links.
        path: str
            The folder to download to.
        """
        payload = {
            'urls' : '\n'.join(links),
            'savepath' : path
        }
        return self.connector.request('POST', '/torrents/add', payload=payload)

    def pause_torrent(self, hash : str):
        """
        Pauses a single torrent.

        Parameters
        ----------
        hash: str
            The hash of the torrent to pause.
        """
        payload = {
            'hashes' : hash
        }
        print(payload)
        return self.connector.request('POST', '/torrents/pause', payload=payload)

    def pause_multi_torrents(self, hashes : list):
        """
        Pauses multiple torrent.

        Parameters
        ----------
        hashes: list
            A list of hashes of the torrents to pause.
        """
        payload = {
            'hashes' : '|'.join(hashes)
        }
        print(payload)
        return self.connector.request('POST', '/torrents/pause', payload=payload)

    def resume_torrent(self, hash : list):
        """
        Resumes a single torrent.

        Parameters
        ----------
        hash: str
            The hash of the torrent to resume.
        """
        payload = {
            'hashes' : hash
        }
        print(payload)
        return self.connector.request('POST', '/torrents/resume', payload=payload)

    def resume_multi_torrents(self, hashes : list):
        """
        Resumes multiple torrent.

        Parameters
        ----------
        hashes: list
            A list of hashes of the torrents to resume.
        """
        payload = {
            'hashes' : '|'.join(hashes)
        }
        print(payload)
        return self.connector.request('POST', '/torrents/resume', payload=payload)
