import json
from core.base_module import BaseModule
from core.logger import logger

class CRTSHRecon(BaseModule):
    def __init__(self):
        self.name = "CRT.sh"
        self.description = "Certificate Transparency Recon"
        self.category = "recon"

    async def run(self, target: str, http_client) -> dict:
        url = f"https://crt.sh/?q=%.{target}&output=json"
        logger.info(f"[{self.name}] Buscando CT logs para: {target}")

        found_domains = set()

        try:
            text = await http_client.get(url, timeout=25)

            if not text or "<html" in text.lower():
                logger.warning(f"[{self.name}] JSON indisponível (fallback bloqueado).")
                return {"source": "crt.sh", "type": "subdomains", "data": []}

            data = json.loads(text)

            for entry in data:
                name_value = entry.get("name_value", "")
                for domain in name_value.split("\n"):
                    domain = domain.lower().strip().replace("*.", "")
                    if domain.endswith(target):
                        found_domains.add(domain)

            logger.info(f"[{self.name}] Subdomínios encontrados: {len(found_domains)}")

        except Exception as e:
            logger.error(f"[{self.name}] Erro: {e}")

        return {
            "source": "crt.sh",
            "type": "subdomains",
            "data": sorted(found_domains)
        }
