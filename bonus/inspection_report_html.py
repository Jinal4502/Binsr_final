#!/usr/bin/env python3
"""
inspection_report_html.py
--------------------------
Drastically faster HTML + WeasyPrint version of inspection_report_structured_fast.py
- Uses Jinja2 templates
- Uses WeasyPrint for PDF generation (HTML/CSS layout engine)
- 10x faster and visually identical
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

INPUT_JSON = "../binsr-challenge/src/inspection.json"
# INPUT_JSON = "https://github.com/ayadav42/binsr-challenge/blob/main/src/inspection.json"
OUTPUT_PDF = "./binsr_customized_inspection_report.pdf"
TEMPLATE_DIR = Path("./templates")
TEMPLATE_FILE = "report_template.html"
# TEMPLATE_FILE = "https://github.com/ayadav42/binsr-challenge/blob/main/src/bonus/templates/report_template.html"

# ---------- SETUP ----------
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def ms_to_date(ms):
    try:
        return datetime.fromtimestamp(int(ms) / 1000).strftime("%B %d, %Y")
    except Exception:
        return "Unknown"

def generate_pdf(data):
    inspection = data.get("inspection", data)
    template = env.get_template(TEMPLATE_FILE)

    # Prepare render context
    context = {
        "inspection": inspection,
        "address": inspection.get("address", {}),
        "client": inspection.get("clientInfo", {}),
        "inspector": inspection.get("inspector", {}),
        "sections": inspection.get("sections", []),
        "date": ms_to_date(inspection.get("schedule", {}).get("date")),
        "now": datetime.now().strftime("%b %d, %Y"),
    }

    html_out = template.render(**context)

    # Generate PDF with WeasyPrint (fast and accurate)
    HTML(string=html_out, base_url=".").write_pdf(
        OUTPUT_PDF,
        stylesheets=[CSS(string="""
            @page {
                margin: 0.5in;
                size: letter;
                @bottom-center {
                    content: "Page " counter(page);
                    font-size: 10px;
                    color: #666;
                }
            }
            body { font-family: Helvetica, sans-serif; color: #222; }
            h1.cover { text-align: center; color: #0B3D91; font-size: 28px; margin-bottom: 5px; }
            h2.section { color: #0B3D91; border-bottom: 2px solid #0B3D91; padding-bottom: 3px; }
            .small-muted { color: #777; font-size: 11px; }
            table { width: 100%; border-collapse: collapse; margin-top: 8px; }
            th, td { border: 1px solid #ddd; padding: 6px; font-size: 12px; vertical-align: top; }
            th { background: #f5f7fb; text-align: left; }
            .legend span { padding: 3px 8px; border-radius: 3px; color: white; margin-right: 5px; }
            .I { background: #8BC34A; }
            .NI { background: #FFB74D; }
            .NP { background: #BDBDBD; }
            .D { background: #EF5350; }
            .comment-block { margin-top: 8px; display: flex; gap: 10px; align-items: flex-start; }
            .comment-block img { width: 200px; height: 150px; object-fit: cover; border: 1px solid #ccc; }
            .comment-text { flex: 1; }
        """)]
    )

    print(f"✅ HTML-based PDF generated: {OUTPUT_PDF}")

# ---------- MAIN ----------
if __name__ == "__main__":
    start = time.time()
    if not Path(INPUT_JSON).exists():
        print(f"❌ Missing file: {INPUT_JSON}")
    else:
        with open(INPUT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("🧩 Generating ultra-fast HTML-based inspection report...")
        generate_pdf(data)
    print(f"⏱️ Done in {time.time() - start:.2f} seconds.")
