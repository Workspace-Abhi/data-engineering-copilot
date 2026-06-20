"""Visualization helpers for rendering premium SVG pipeline lineage and flowcharts."""

def get_glow_filter():
    """Return common SVG filter definitions for drop shadows and glow effects."""
    return """
    <defs>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.3"/>
        </filter>
        <linearGradient id="activeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8" />
            <stop offset="100%" stop-color="#6366f1" />
        </linearGradient>
        <linearGradient id="inactiveGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#334155" />
            <stop offset="100%" stop-color="#1e293b" />
        </linearGradient>
        <linearGradient id="successGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#34d399" />
            <stop offset="100%" stop-color="#059669" />
        </linearGradient>
        <linearGradient id="errorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#f87171" />
            <stop offset="100%" stop-color="#dc2626" />
        </linearGradient>
    </defs>
    """

def render_data_lineage(active_stage: str = "Bronze") -> str:
    """Generate SVG representation of Data Engineering Pipeline Lineage.
    
    Stages: Source, ADF, Bronze, Silver, Gold
    """
    stages = ["Source", "ADF", "Bronze", "Silver", "Gold"]
    labels = {
        "Source": "Source DB / ADLS",
        "ADF": "ADF Orchestrator",
        "Bronze": "Bronze (Raw Delta)",
        "Silver": "Silver (SCD Type 2)",
        "Gold": "Gold (Dataverse / Target)"
    }
    descriptions = {
        "Source": "Ingestion origin",
        "ADF": "Incremental loads",
        "Bronze": "Raw landing zone",
        "Silver": "Cleaned history",
        "Gold": "Business summaries"
    }

    svg_width = 850
    svg_height = 140
    
    svg = f'<svg width="100%" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">'
    svg += get_glow_filter()
    
    # Render connection lines first
    for i in range(len(stages) - 1):
        x1 = 90 + i * 165 + 110
        y1 = 70
        x2 = x1 + 55
        y2 = 70
        is_passed = stages.index(active_stage) > i
        line_color = "#38bdf8" if is_passed else "#475569"
        line_dash = "" if is_passed else 'stroke-dasharray="4,4"'
        svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{line_color}" stroke-width="3" {line_dash} />'
        # Add a tiny arrow
        svg += f'<polygon points="{x2},{y2} {x2-8},{y2-4} {x2-8},{y2+4}" fill="{line_color}" />'

    # Render Node Blocks
    for i, stage in enumerate(stages):
        x = 90 + i * 165
        y = 35
        w = 110
        h = 70
        
        is_active = (stage == active_stage)
        is_passed = stages.index(active_stage) >= i
        
        # Determine background
        if is_active:
            fill_style = "url(#activeGrad)"
            stroke_style = "#60a5fa"
            stroke_width = 2
            effect = 'filter="url(#glow)"'
            text_color = "#ffffff"
            desc_color = "#e2e8f0"
        elif is_passed:
            fill_style = "url(#successGrad)"
            stroke_style = "#34d399"
            stroke_width = 1.5
            effect = 'filter="url(#shadow)"'
            text_color = "#ffffff"
            desc_color = "#cbd5e1"
        else:
            fill_style = "url(#inactiveGrad)"
            stroke_style = "#475569"
            stroke_width = 1
            effect = ""
            text_color = "#94a3b8"
            desc_color = "#64748b"
            
        svg += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" ry="10" fill="{fill_style}" stroke="{stroke_style}" stroke-width="{stroke_width}" {effect} style="transition: all 0.3s ease;" />'
        
        # Add labels
        svg += f'<text x="{x + w/2}" y="{y + 28}" text-anchor="middle" fill="{text_color}" font-family="system-ui, -apple-system" font-size="11" font-weight="bold">{labels[stage]}</text>'
        svg += f'<text x="{x + w/2}" y="{y + 48}" text-anchor="middle" fill="{desc_color}" font-family="system-ui, -apple-system" font-size="9" opacity="0.85">{descriptions[stage]}</text>'

    svg += "</svg>"
    return svg

def render_adf_flow(source_table: str = "dbo.SourceTable", target_table: str = "dbo.TargetTable", watermark_col: str = "ModifiedDate") -> str:
    """Generate SVG flowchart representation of an Azure Data Factory Watermark Pipeline."""
    svg_width = 750
    svg_height = 200
    
    svg = f'<svg width="100%" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">'
    svg += get_glow_filter()
    
    # Blocks
    # 1. Lookup Old (x=40, y=20)
    # 2. Lookup New (x=40, y=110)
    # 3. Copy Data (x=270, y=65)
    # 4. Stored Procedure (x=500, y=65)
    
    # Connections
    # 1 -> 3
    svg += '<path d="M 190 55 L 230 55 L 230 100 L 270 100" fill="none" stroke="#6366f1" stroke-width="2" />'
    # 2 -> 3
    svg += '<path d="M 190 145 L 230 145 L 230 100 L 270 100" fill="none" stroke="#6366f1" stroke-width="2" />'
    # 3 -> 4
    svg += '<line x1="420" y1="100" x2="500" y2="100" stroke="#34d399" stroke-width="3" />'
    svg += '<polygon points="500,100 492,96 492,104" fill="#34d399" />'
    
    # Draw boxes
    # Lookup Old
    svg += '<rect x="40" y="20" width="150" height="70" rx="8" ry="8" fill="url(#inactiveGrad)" stroke="#6366f1" stroke-width="1.5" filter="url(#shadow)" />'
    svg += '<text x="115" y="48" text-anchor="middle" fill="#ffffff" font-family="system-ui" font-size="11" font-weight="bold">🔍 Lookup Old WM</text>'
    svg += f'<text x="115" y="65" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="9">{watermark_col}</text>'
    
    # Lookup New
    svg += '<rect x="40" y="110" width="150" height="70" rx="8" ry="8" fill="url(#inactiveGrad)" stroke="#6366f1" stroke-width="1.5" filter="url(#shadow)" />'
    svg += '<text x="115" y="138" text-anchor="middle" fill="#ffffff" font-family="system-ui" font-size="11" font-weight="bold">🔍 Lookup Max Src</text>'
    svg += f'<text x="115" y="155" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="9">MAX({watermark_col})</text>'
    
    # Copy Data
    src_table_short = source_table.split(".")[-1]
    tgt_table_short = target_table.split(".")[-1]
    svg += '<rect x="270" y="65" width="150" height="70" rx="8" ry="8" fill="url(#activeGrad)" stroke="#38bdf8" stroke-width="2" filter="url(#glow)" />'
    svg += f'<text x="345" y="93" text-anchor="middle" fill="#ffffff" font-family="system-ui" font-size="12" font-weight="bold">📋 Copy {src_table_short} ➔ {tgt_table_short}</text>'
    svg += f'<text x="345" y="110" text-anchor="middle" fill="#e2e8f0" font-family="system-ui" font-size="9">where {watermark_col} &gt; old_wm</text>'
    
    # Update Watermark
    svg += '<rect x="500" y="65" width="160" height="70" rx="8" ry="8" fill="url(#successGrad)" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)" />'
    svg += '<text x="580" y="93" text-anchor="middle" fill="#ffffff" font-family="system-ui" font-size="11" font-weight="bold">🔄 Update Control DB</text>'
    svg += f'<text x="580" y="110" text-anchor="middle" fill="#cbd5e1" font-family="system-ui" font-size="9">Set {tgt_table_short} watermark</text>'
    
    svg += "</svg>"
    return svg

def render_reconciliation_chart(source: int, target: int, missing_t: int, missing_s: int) -> str:
    """Generate SVG comparison chart for SQL Data Reconciliation."""
    total = max(source, target, 1)
    
    # Calculate bar widths
    max_bar_width = 300
    src_w = int((source / total) * max_bar_width)
    tgt_w = int((target / total) * max_bar_width)
    
    # Determine gradient/color status
    color_src = "url(#activeGrad)"
    color_tgt = "url(#successGrad)" if source == target else "url(#errorGrad)"
    
    svg_width = 500
    svg_height = 150
    
    svg = f'<svg width="100%" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">'
    svg += get_glow_filter()
    
    # Source Bar
    svg += '<text x="10" y="35" fill="#e2e8f0" font-family="system-ui" font-size="12" font-weight="bold">Source Record Count</text>'
    svg += f'<rect x="150" y="20" width="{src_w}" height="20" rx="4" ry="4" fill="{color_src}" filter="url(#shadow)" />'
    svg += f'<text x="{150 + src_w + 10}" y="35" fill="#38bdf8" font-family="system-ui" font-size="12" font-weight="bold">{source}</text>'
    
    # Target Bar
    svg += '<text x="10" y="75" fill="#e2e8f0" font-family="system-ui" font-size="12" font-weight="bold">Target Record Count</text>'
    svg += f'<rect x="150" y="60" width="{tgt_w}" height="20" rx="4" ry="4" fill="{color_tgt}" filter="url(#shadow)" />'
    svg += f'<text x="{150 + tgt_w + 10}" y="75" fill="#10b981" font-family="system-ui" font-size="12" font-weight="bold">{target}</text>'
    
    # Discrepancy Text Indicators
    y_offset = 120
    if missing_t > 0:
        svg += f'<rect x="10" y="{y_offset - 12}" width="12" height="12" rx="3" ry="3" fill="url(#errorGrad)" />'
        svg += f'<text x="28" y="{y_offset - 2}" fill="#f87171" font-family="system-ui" font-size="11">Missing in Target: {missing_t} rows</text>'
    if missing_s > 0:
        x_offset = 240 if missing_t > 0 else 10
        svg += f'<rect x="{x_offset}" y="{y_offset - 12}" width="12" height="12" rx="3" ry="3" fill="url(#errorGrad)" />'
        svg += f'<text x="{x_offset + 18}" y="{y_offset - 2}" fill="#f87171" font-family="system-ui" font-size="11">Stale in Target: {missing_s} rows</text>'
        
    if missing_t == 0 and missing_s == 0:
        svg += f'<rect x="10" y="{y_offset - 12}" width="12" height="12" rx="3" ry="3" fill="url(#successGrad)" />'
        svg += f'<text x="28" y="{y_offset - 2}" fill="#34d399" font-family="system-ui" font-size="11" font-weight="bold">✅ In Sync - Zero mismatches detected</text>'
        
    svg += "</svg>"
    return svg
