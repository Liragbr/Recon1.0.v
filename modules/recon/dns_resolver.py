import asyncio
import dns.resolver
from functools import partial
from core.base_module import BaseModule
from core.logger import logger

class DNSResolver(BaseModule):
    def __init__(self):
        self.name = "DNS Resolver"
        self.description = "Robust DNS Recon (A, MX, NS, TXT)"
        self.category = "infra"
        self.record_types = ["A", "MX", "NS", "TXT"]

    def _resolver(self):
        r = dns.resolver.Resolver()
        r.timeout = 5
        r.lifetime = 5
        r.nameservers = ["1.1.1.1", "8.8.8.8"]
        return r

    def _query(self, target, record):
        try:
            resolver = self._resolver()
            return list(resolver.resolve(target, record))
        except:
            return []

    async def run(self, target: str, http_client) -> dict:
        logger.info(f"[{self.name}] Resolvendo DNS para: {target}")
        loop = asyncio.get_running_loop()

        tasks = [
            loop.run_in_executor(None, partial(self._query, target, r))
            for r in self.record_types
        ]

        results = await asyncio.gather(*tasks)
        found = []

        for i, r_type in enumerate(self.record_types):
            for ans in results[i]:
                raw = ans.to_text().replace('"', '')

                if r_type == "A":
                    found.append(f"IP: {raw}")
                elif r_type == "MX":
                    found.append(f"Mail: {raw.split()[-1]}")
                elif r_type == "NS":
                    found.append(f"NS: {raw}")
                elif r_type == "TXT":
                    found.append(f"TXT: {raw[:80]}")

        if found:
            logger.info(f"[{self.name}] Registros DNS encontrados: {len(found)}")
        else:
            logger.warning(f"[{self.name}] Nenhum registro retornado")

        return {
            "source": "dns_resolver",
            "type": "infra_records",
            "data": found
        }
