import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logger(level="INFO"):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    return logging.getLogger("redrecon")

logger = setup_logger()