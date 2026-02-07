import aiohttp
import asyncio
from core.logger import logger
from core.config import Config

class AsyncHTTP:
    def __init__(self):
        self.session = None

    async def start(self):
        timeout = aiohttp.ClientTimeout(total=Config.TIMEOUT)
        connector = aiohttp.TCPConnector(limit=Config.CONCURRENCY, ssl=False)
        self.session = aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout,
            headers={"User-Agent": Config.USER_AGENT}
        )

    async def get(self, url: str, params: dict = None, **kwargs):
        if not self.session: await self.start()
        try:
            async with self.session.get(url, params=params, **kwargs) as response:
                if response.status in [401, 403]:
                    logger.warning(f"[yellow]Auth Error:[/yellow] {url}")
                try:
                    return await response.json()
                except:
                    return await response.text()
        except Exception as e:
            logger.debug(f"Falha em {url}: {e}")
            return None

    async def close(self):
        if self.session: await self.session.close()