from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def export_to_pdf(results, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>Compliance Report</b>", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Total Violations: {results.get('total_violations', 0)}", styles["Normal"]))

    for severity, violations in results.get("violations", {}).items():
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>{severity}</b>", styles["Heading3"]))
        for v in violations:
            elements.append(Paragraph(f"• {v.get('description', 'No description')}", styles["Normal"]))

    doc.build(elements)
    print(f"📄 PDF generated: {output_path}")