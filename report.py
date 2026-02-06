from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(summary, results, filename="report.pdf"):
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Contract Risk Report", styles["Heading1"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(summary, styles["BodyText"]))
    story.append(Spacer(1, 30))

    for r in results:
        if r["risk"] != "Low":
            story.append(
                Paragraph(f"Clause {r['id']} — Risk: {r['risk']}", styles["Heading2"])
            )
            story.append(Paragraph(r["explanation"], styles["BodyText"]))
            story.append(Spacer(1, 20))

    doc = SimpleDocTemplate(filename)
    doc.build(story)
