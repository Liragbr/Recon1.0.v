import asyncio
from core.base_module import BaseModule
from core.logger import logger

class PortScanner(BaseModule):
    def __init__(self):
        self.name = "Port Scanner"
        self.description = "Async TCP Port Scan (Top 100)"
        self.category = "active"

        self.ports = [
            21,22,23,25,53,80,110,139,143,443,
            445,3389,3306,5432,8080,8443,5900
        ]

    async def scan_port(self, host, port):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=3.0
            )
            writer.close()
            await writer.wait_closed()
            return port
        except:
            return None

    async def run(self, target: str, http_client) -> dict:
        logger.info(f"[{self.name}] Scanning portas TCP em {target}")

        tasks = [self.scan_port(target, p) for p in self.ports]
        results = await asyncio.gather(*tasks)

        open_ports = sorted([p for p in results if p])

        if open_ports:
            logger.info(f"[{self.name}] Portas abertas detectadas: {open_ports}")
        else:
            logger.warning(f"[{self.name}] Nenhuma porta aberta detectada")

        return {
            "source": "port_scan",
            "type": "open_ports",
            "data": open_ports
        }
