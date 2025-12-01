import json, csv
from datetime import datetime
from pathlib import Path
from .html_template import HTML_TEMPLATE
from .pdf_generator import export_to_pdf

def export_to_json(results, output_path):
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"💾 JSON saved → {output_path}")

def export_to_csv(results, output_path):
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID","Severity","Description","Policy Reference","Remediation"])
        vid = 1
        for severity, violations in results.get("violations", {}).items():
            for v in violations:
                writer.writerow([
                    f"V{vid:03d}",
                    severity,
                    v.get("description", ""),
                    v.get("policy_ref", ""),
                    v.get("remediation", "")
                ])
                vid += 1
    print(f"📄 CSV saved → {output_path}")

def export_to_html(results, output_path):
    violations_html = ""
    for severity, violations in results.get("violations", {}).items():
        for v in violations:
            violations_html += f"""
<div class="violation {severity.lower()}">
<span class="severity-badge {severity.lower()}">{severity}</span>
<h3>{v.get('description', 'Violation')}</h3>
<p><b>Policy Reference:</b> {v.get('policy_ref', 'N/A')}</p>
<p><b>Remediation:</b> {v.get('remediation', 'N/A')}</p>
</div>
"""
    html = HTML_TEMPLATE.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_violations=results.get("total_violations", 0),
        critical_count=results["severity_counts"].get("CRITICAL", 0),
        high_count=results["severity_counts"].get("HIGH", 0),
        medium_count=results["severity_counts"].get("MEDIUM", 0),
        low_count=results["severity_counts"].get("LOW", 0),
        violations_html=violations_html,
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🌐 HTML saved → {output_path}")

def export_all(results, base_name, output_dir, fmt="all"):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"{base_name}_{ts}.json"
    csv_path = output_dir / f"{base_name}_{ts}.csv"
    html_path = output_dir / f"{base_name}_{ts}.html"
    pdf_path = output_dir / f"{base_name}_{ts}.pdf"

    if fmt in ["json", "all"]: export_to_json(results, json_path)
    if fmt in ["csv", "all"]: export_to_csv(results, csv_path)
    if fmt in ["html", "all"]: export_to_html(results, html_path)
    if fmt in ["pdf", "all"]: export_to_pdf(results, pdf_path)

    print("\n✔ Export completed!")
