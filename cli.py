import asyncio
import argparse
import sys
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from core.http import AsyncHTTP
from core.plugin_loader import PluginLoader
from core.logger import logger
from core.report import ReportGenerator

console = Console()

BANNER_ART = r"""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗        ██╗     ██╗    ██████╗     ██████╗ ██╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║       ██╔╝    ███║   ██╔═████╗   ██╔═████╗██║   ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║      ██╔╝     ╚██║   ██║██╔██║   ██║██╔██║██║   ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║     ██╔╝       ██║   ████╔╝██║   ████╔╝██║╚██╗ ██╔╝
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║    ██╔╝        ██║██╗╚██████╔╝██╗╚██████╔╝ ╚████╔╝ 
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝         ╚═╝╚═╝ ╚═════╝ ╚═╝ ╚═════╝   ╚═══╝  
"""

def print_banner():
    console.clear()
    console.print(Align.center(Text(BANNER_ART, style="bold red")))
    console.print(Align.center(Text("[ v1.0.0 ] [ RED TEAM OPS ] [ ASYNC CORE ]", style="bold white dim")))
    console.print(Text("─" * console.width, style="dim red"))
    print()

def print_target_intel(target, plugins_count):
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    grid.add_row(
        f"[bold cyan]TARGET SYSTEM:[/bold cyan] {target}",
        f"[bold green]START TIME:[/bold green] {datetime.now().strftime('%H:%M:%S')}"
    )
    grid.add_row(
        f"[bold cyan]ACTIVE PLUGINS:[/bold cyan] {plugins_count}",
        "[bold red]OPSEC LEVEL:[/bold red] [blink]HIGH[/blink]"
    )

    console.print(Panel(
        grid,
        title="[bold yellow]MISSION PARAMETERS[/bold yellow]",
        border_style="red",
        padding=(1, 2)
    ))
    print()

def format_results(results):
    table = Table(title="[bold red]EXFILTRATED INTELLIGENCE[/bold red]", border_style="dim white", show_lines=True)
    
    table.add_column("Plugin", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Data Points", style="green")
    table.add_column("Status", style="bold white")

    for res in results:
        if isinstance(res, Exception):
            table.add_row("Unknown", "Error", "0", f"[red]FAILED[/red]")
            continue
        
        if not res:
            continue

        source = res.get("source", "Unknown")
        dtype = res.get("type", "Info")
        data = res.get("data", [])

        if isinstance(data, list):
            content = f"{len(data)} records found"
            if 0 < len(data) <= 15:
                content = ", ".join(map(str, data))
        else:
            content = str(data)

        table.add_row(source.upper(), dtype.upper(), content, "[green]SUCCESS[/green]")

    console.print(table)

async def main():
    parser = argparse.ArgumentParser(description="RedRecon Pro CLI")
    parser.add_argument("-t", "--target", required=True, help="Target Domain")
    args = parser.parse_args()

    print_banner()

    http = AsyncHTTP()
    loader = PluginLoader()
    plugins = loader.load_all()

    if not plugins:
        console.print("[bold red][!] CRITICAL: No modules loaded. Aborting.[/bold red]")
        return

    print_target_intel(args.target, len(plugins))

    results = []
    start_time = time.time()

    with Progress(
        SpinnerColumn(style="bold red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=None, complete_style="red"),
        TextColumn("{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:

        task = progress.add_task("[cyan]Initializing Async Engine...", total=len(plugins))

        await http.start()

        tasks = [plugin.run(args.target, http) for plugin in plugins]

        for future in asyncio.as_completed(tasks):
            try:
                res = await future
            except Exception as e:
                res = e
            
            results.append(res)
            name = res.get("source", "Unknown") if isinstance(res, dict) else "Error"
            progress.update(task, description=f"[bold green]Harvesting:[/bold green] {name}")
            progress.advance(task)

    await http.close()

    print()
    format_results(results)

    elapsed = time.time() - start_time
    console.print(f"\n[dim]Scan finished in {elapsed:.2f}s[/dim]")

    report = ReportGenerator()
    report_file = report.generate(args.target, {r["source"]: r["data"] for r in results if isinstance(r, dict)})

    console.print(f"[bold green][+] Report generated:[/bold green] {report_file}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red][!] INTERRUPTED BY USER[/bold red]")