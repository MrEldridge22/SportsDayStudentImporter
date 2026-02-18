import pandas as pd
import json


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


# Change this for each year as needed
year = 2026

# Read in Student students_df from Timetabling Solutions V10 Development File
tfx_file = f"TTD_{year}_S1.tfx"
with open(tfx_file) as f:
    tfx_data = json.load(f)

students_df = pd.DataFrame(tfx_data['Students'])

# Drop Unnecessary Columns
students_df = students_df.drop(columns=['Name',
                                        'StudentID',
                                        'RollClass',
                                        'Email',
                                        'FileName',
                                        'StudentLessons',
                                        'StudyStream',
                                        'SubmitOrder',
                                        'BOSCode','MiddleName'])
# Rename Columns Ready for Import
students_df = students_df.rename(columns={
                                        'FirstName': 'First Name',
                                        'LastName': 'Last Name',
                                        'Code': 'Student ID',
                                        'YearLevel': 'Year',
                                        'HomeGroup': 'Group'})

# Remove leading zeros from Year, convert to int
students_df['Year'] = students_df['Year'].astype(str).str.lstrip('0').astype(int)

students_df = students_df.sort_values(by=['Year', 'Group', 'First Name']).reset_index(drop=True)
students_df['Gender'] = students_df['Gender'].map({'M': 'Male', 'F': 'Female'})

# Base number per Year
base_map = {
    7: 7000,
    8: 8000,
    9: 9000,
    10: 1000,   # "1 + 3-digit sequence" -> 1001, 1002, ...
    11: 1501,   # Special: starts at 1500 (not 1501)
    12: 2000    # "2 + 3-digit sequence" -> 2001, 2002, ...
}

# Map base; other year levels, handle them before this or they will become NaN
students_df['__base'] = students_df['Year'].map(base_map)

# Sequence within each Year following the sorted order
students_df['__seq'] = students_df.groupby('Year').cumcount() + 1  # 1,2,3,...

# Compute Competitor Number
# For Year 11, first should be 1500 (i.e., don't add the +1 effect): subtract 1 for Year 11 only
students_df['Competitor Number'] = (
    students_df['__base'] + students_df['__seq'] - (students_df['Year'] == 11).astype(int)
).astype('Int64')

# Clean up helper columns
students_df = students_df.drop(columns=['__base', '__seq'])

# Save back out for import into Scoring System.
students_df.to_csv('Participant ID Upload.csv', index=False)
# print(students_df)


# PDF Output

# Assuming `data` is your sorted DataFrame with columns:
# ['Year', 'Group', 'Surname', 'FirstName', 'Competitor Number']

output_pdf = "Care Class Lists.pdf"

styles = getSampleStyleSheet()

group_title_style = ParagraphStyle(
    name="GroupTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=22,        # Adjust size to taste (e.g., 22–26)
    leading=26,
    alignment=1,        # 0=left, 1=center, 2=right
    spaceAfter=6
)

# Optional: a subtle subtitle style (remove if you don’t want a subtitle line)
subtitle_style = ParagraphStyle(
    name="Subtitle",
    parent=styles["Normal"],
    fontSize=14,
    textColor=colors.grey,
    alignment=1,
    spaceAfter=6
)


body_style = styles['BodyText']
body_style.fontSize = 10

elements = []

# Iterate groups and add a page per group
for group_name, df_g in students_df.groupby('Group', sort=True):
    # --- Title (group name only, big and centered) ---
    elements.append(Paragraph(str(group_name), group_title_style))
    elements.append(Spacer(1, 6))  # a little breathing room

    elements.append(Paragraph(f"{year} Sports Day Participant IDs", subtitle_style))
    elements.append(Spacer(1, 6))

    # Build table data
    table_data = [["Competitor Number", "First Name", "Last Name", "Year"]]
    for _, row in df_g[['Competitor Number', 'First Name', 'Last Name', 'Year']].iterrows():
        table_data.append([str(row['Competitor Number']), str(row['First Name']), str(row['Last Name']), str(row['Year'])])

    # Create table with styling
    tbl = Table(table_data, colWidths=[30*mm, 50*mm, 50*mm, 15*mm])
    tbl.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    elements.append(tbl)
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Total students: {len(df_g)}", subtitle_style))
    elements.append(PageBreak())

# Build the PDF
doc = SimpleDocTemplate(
    output_pdf,
    pagesize=A4,
    rightMargin=18*mm, leftMargin=18*mm,
    topMargin=18*mm, bottomMargin=18*mm
)
doc.build(elements)
