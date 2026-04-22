from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(name, role, skills, gap, match_score):
    doc = SimpleDocTemplate("career_report.pdf")

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"<b>Career Report</b>", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Name:</b> {name}", styles["Normal"]))
    content.append(Paragraph(f"<b>Target Role:</b> {role}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Top Skills:</b>", styles["Heading2"]))
    for s in skills:
        content.append(Paragraph(f"- {s}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Skill Gap:</b>", styles["Heading2"]))
    for g in gap:
        content.append(Paragraph(f"- {g}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Match Score:</b> {match_score}%", styles["Normal"]))

    doc.build(content)

    return "career_report.pdf"