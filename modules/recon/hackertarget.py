from core.base_module import BaseModule
from core.logger import logger

class HackerTargetRecon(BaseModule):
    def __init__(self):
        self.name = "HackerTarget"
        self.description = "Passive Subdomain Recon (HackerTarget)"
        self.category = "recon"

    def extract_root_domain(self, domain):
        parts = domain.lower().split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return domain

    async def run(self, target: str, http_client) -> dict:
        url = f"https://api.hackertarget.com/hostsearch/?q={target}"
        logger.info(f"[{self.name}] Consultando HackerTarget API")

        found = set()

        try:
            text = await http_client.get(url, timeout=20)

            if not text or "error" in text.lower():
                logger.warning(f"[{self.name}] API retornou vazio")
                return {"source": "hackertarget", "type": "subdomains", "data": []}

            root_domain = self.extract_root_domain(target)

            for line in text.splitlines():
                host = line.split(",")[0].strip().lower()

                if host.endswith(root_domain):
                    found.add(host)

            logger.info(f"[{self.name}] Subdomínios encontrados: {len(found)}")

        except Exception as e:
            logger.error(f"[{self.name}] Erro: {e}")

        return {
            "source": "hackertarget",
            "type": "subdomains",
            "data": sorted(found)
        }
