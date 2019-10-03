class QBittorrentError(Exception):
    """
    A generic QBittorrent error.
    """
    pass

class TorrentNotValid(QBittorrentError):
    """
    Torrent file is not valid
    """
    pass

class TorrentHashNotFound(QBittorrentError):
    """
    Torrent hash was not found or invalid
    """
    pass

class FailedLogin(QBittorrentError):
    """
    Something went wrong with login
    """
    pass

class HttpException(QBittorrentError):
    """
    Something went wrong with login
    """
    pass