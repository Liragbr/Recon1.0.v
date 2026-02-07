import json
import os
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    def __init__(self, output_dir="results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, target: str, results: dict):
        stats = self._calculate_stats(results)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = self.output_dir / f"report_{target.replace('.', '_')}.html"
        html_content = self._build_html(target, timestamp, results, stats)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(filename)

    def _calculate_stats(self, results):
        stats = {
            "total_assets": 0,
            "open_ports": 0,
            "subdomains": 0,
            "vulns": 0
        }
        
        for source, data in results.items():
            count = len(data) if isinstance(data, list) else 1
            source_lower = source.lower()
            
            if "port" in source_lower:
                stats["open_ports"] += count
            elif "crt" in source_lower or "hacker" in source_lower:
                stats["subdomains"] += count
            
            stats["total_assets"] += count
            
        return stats

    def _build_html(self, target, timestamp, results, stats):
        plugin_sections = ""
        for source, data in results.items():
            plugin_sections += self._render_plugin_card(source, data)

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RECON// {target}</title>
    
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg-dark: #0d1117;
            --bg-card: #161b22;
            --border: #30363d;
            --text-main: #c9d1d9;
            --text-dim: #8b949e;
            --accent: #58a6ff;
            --success: #238636;
            --danger: #f85149;
            --warning: #d29922;
        }}

        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 20px;
        }}

        /* Header Tático */
        .header {{
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .brand {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--danger);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .target-info {{
            text-align: right;
            font-size: 0.9rem;
            color: var(--text-dim);
        }}

        /* Dashboard Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}

        .stat-value {{
            display: block;
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent);
            font-family: 'JetBrains Mono', monospace;
        }}

        .stat-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-dim);
        }}

        /* Seções de Resultados */
        .plugin-section {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 30px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}

        .plugin-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
        }}

        .plugin-title {{
            font-family: 'JetBrains Mono', monospace;
            color: var(--success);
            font-size: 1.2rem;
            text-transform: uppercase;
        }}

        /* DataTables Customization */
        table.dataTable {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            border-collapse: collapse !important;
            width: 100% !important;
        }}
        
        table.dataTable tbody tr {{ background-color: var(--bg-dark) !important; }}
        table.dataTable tbody td {{ border-bottom: 1px solid var(--border); padding: 12px; }}
        
        .dataTables_wrapper .dataTables_length, 
        .dataTables_wrapper .dataTables_filter, 
        .dataTables_wrapper .dataTables_info, 
        .dataTables_wrapper .dataTables_paginate {{
            color: var(--text-dim) !important;
            margin-top: 10px;
        }}

        .dataTables_wrapper .dataTables_filter input {{
            background: var(--bg-dark);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 5px;
            border-radius: 4px;
        }}

        /* Badges */
        .badge {{
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        .badge-port {{ background: rgba(88, 166, 255, 0.2); color: var(--accent); }}
        .badge-crit {{ background: rgba(248, 81, 73, 0.2); color: var(--danger); }}

    </style>
</head>
<body>

    <div class="header">
        <div class="brand">RECON <span style="color:white">//</span> 1.0.0V</div>
        <div class="target-info">
            <div>TARGET: <strong style="color: white;">{target}</strong></div>
            <div>SCAN ID: {int(datetime.now().timestamp())}</div>
            <div>DATE: {timestamp}</div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-value">{stats['total_assets']}</span>
            <span class="stat-label">Total Assets</span>
        </div>
        <div class="stat-card">
            <span class="stat-value" style="color: var(--success);">{stats['subdomains']}</span>
            <span class="stat-label">Subdomains</span>
        </div>
        <div class="stat-card">
            <span class="stat-value" style="color: var(--danger);">{stats['open_ports']}</span>
            <span class="stat-label">Open Ports</span>
        </div>
        <div class="stat-card">
            <span class="stat-value" style="color: var(--warning);">HIGH</span>
            <span class="stat-label">Threat Level</span>
        </div>
    </div>

    <div class="content">
        {plugin_sections}
    </div>

    <footer style="text-align: center; color: var(--text-dim); margin-top: 50px; font-size: 0.8rem;">
        GENERATED BY RECON 1.0.0V • CONFIDENTIAL
    </footer>

    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function() {{
            $('.result-table').DataTable({{
                "paging": true,
                "ordering": true,
                "info": true,
                "pageLength": 10,
                "language": {{
                    "search": "FILTER RESULTS:",
                    "lengthMenu": "SHOW _MENU_"
                }}
            }});
        }});
    </script>
</body>
</html>
"""

    def _render_plugin_card(self, source, data):
        rows = ""
        
        if isinstance(data, list):
            for item in data:
          
                val_str = str(item)
                if source == "port_scan" and val_str in ['21', '22', '3389', '445']:
                    item_html = f"<span class='badge badge-crit'>{val_str}</span> <span style='color:var(--danger)'>CRITICAL SERVICE</span>"
                elif source == "port_scan":
                    item_html = f"<span class='badge badge-port'>{val_str}</span> TCP OPEN"
                else:
                    item_html = val_str
                
                rows += f"<tr><td>{item_html}</td></tr>"
        
        elif isinstance(data, dict):
            for k, v in data.items():
                rows += f"<tr><td><strong>{k}</strong>: {v}</td></tr>"
        else:
            rows = f"<tr><td>{data}</td></tr>"

        if not rows:
            rows = "<tr><td style='color: var(--text-dim)'>No data found during this scan.</td></tr>"

        return f"""
        <div class="plugin-section">
            <div class="plugin-header">
                <div class="plugin-title">MODULE :: {source.upper()}</div>
                <div class="badge">{len(data) if isinstance(data, list) else 1} ITEMS</div>
            </div>
            <table class="result-table display">
                <thead>
                    <tr><th>EXTRACTED DATA</th></tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """