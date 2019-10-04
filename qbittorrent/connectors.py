
def not_a_real_class(you_messed_up):
    class FailedConnector:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError(you_messed_up)
    return FailedConnector

try:
    import aiohttp
    import asyncio

    class AConnector:
        def __init__(self, session=None, loop=None):
            self.session = session or aiohttp.ClientSession(loop=loop)
            self.loop = loop or asyncio.get_event_loop()
except ImportError:
    AConnector = not_a_real_class("aiohttp not installed :(")
