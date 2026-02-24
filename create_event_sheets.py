# Import required libraries for data processing and PDF creation
import pandas as pd  # For reading and processing CSV files

# Import ReportLab components for creating PDFs
from reportlab.lib.pagesizes import A4  # Sets the page size to A4
from reportlab.lib import colors  # Provides color options (lightblue, lightgrey, etc.)
from reportlab.lib.units import mm  # Allows us to measure things in millimeters
from reportlab.pdfgen import canvas  # Basic PDF drawing functionality
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak  # Advanced PDF layout tools
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # Text formatting styles

# === STEP 1: READ AND PROCESS THE EVENT DATA ===
# Read the carnival program from a CSV file into a data table
event_list = pd.read_csv('CarnivalProgram.csv')

# Split the 'Time' column into separate 'Date' and 'Start Time' columns
# This makes it easier to display the information clearly on each event sheet
event_list['Date'] = event_list['Time'].str.split(' ', expand=True)[0]  # Everything before the first space becomes the date
event_list['Start Time'] = event_list['Time'].str.split(' ', expand=True)[1]  # Everything after the first space becomes the time

# Remove the original combined 'Time' column since we now have separate date and time columns
event_list.drop(columns=['Time'], inplace=True)

# Split the 'Event' column into three separate, clearer columns
# The original format is something like "100m Sprint, Year 8, Boys"
event_list['Event Name'] = event_list['Event'].str.split(',', expand=True)[0]  # "100m Sprint"
event_list['Year Level'] = event_list['Event'].str.split(',', expand=True)[1]  # " Year 8"
event_list['Gender'] = event_list['Event'].str.split(',', expand=True)[2]  # " Boys"

# Remove the original combined 'Event' column since we now have separate columns
event_list.drop(columns=['Event'], inplace=True)

# Clean up the text in the Year Level and Gender columns
# Remove extra spaces and standardize the formatting
event_list['Year Level'] = event_list['Year Level'].str.replace(' grade ', 'Year ')  # Change "grade" to "Year"
event_list['Year Level'] = event_list['Year Level'].str.replace(' grades ', 'Year ')  # Handle plural form
event_list['Year Level'] = event_list['Year Level'].str.strip()  # Remove leading/trailing spaces
event_list['Gender'] = event_list['Gender'].str.strip()  # Remove leading/trailing spaces

# Sort the events by Event Name, Time, and Gender
event_list.sort_values(by=['Event Name', 'Start Time', 'Gender'], inplace=True)

# === STEP 2: SET UP THE PDF DOCUMENT ===
# Create a PDF file that will contain all the event sheets for scoring

# Define the name of the PDF file that will be created
pdf_filename = "Event_Sheets.pdf"
# Create a PDF document object with A4 page size (standard paper size)
doc = SimpleDocTemplate(pdf_filename, pagesize=A4)

# Get the default text styles provided by ReportLab
# These include things like 'Title', 'Normal', 'Heading1', etc.
styles = getSampleStyleSheet()

# === STEP 3: CREATE CUSTOM TEXT STYLES ===
# Define how different parts of text should look (font size, alignment, spacing)

# Style for event names - large, centered, bold
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],  # Base it on the default title style
    fontSize=20,  # Make the text 20 points large
    alignment=1,  # Center the text (0=left, 1=center, 2=right)
    spaceBefore=20,  # Add space above the title
    spaceAfter=10   # Add space below the title
)

# Style for year level and gender - medium size, centered
subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],  # Base it on normal text style
    fontSize=14,  # Medium-sized text
    alignment=1,  # Center the text
    spaceBefore=5,  # Small space above
    spaceAfter=20   # Larger space below
)

# Style for event numbers - medium size, right-aligned, bold
event_number_style = ParagraphStyle(
    'EventNumber',
    parent=styles['Normal'],
    fontSize=16,  # Slightly larger than normal
    alignment=2,  # Right-align the text
    fontName='Helvetica-Bold'  # Make it bold
)
# Style for Start Time - small size, right-aligned, bold
start_time_style = ParagraphStyle(
    'StartTime',
    parent=styles['Normal'],
    fontSize=12,  # Slightly larger than normal
    alignment=2,  # Right-align the text
    fontName='Helvetica-Bold'  # Make it bold
)

# Style for Footer - small size, centered, italic
footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=12,  # Slightly larger than normal
    alignment=1,  # Center the text
    fontName='Helvetica-Oblique'  # Make it italic
)

# === STEP 4: CREATE CONTENT FOR EACH EVENT SHEET ===
# Create a list to hold all the content that will go into the PDF
# Think of this as building blocks - we'll stack paragraphs, tables, and spacing
story = []

# Go through each event in our data table and create a page for it
# This loop will run once for each event (100m sprint, shot put, etc.)
for index, event_row in event_list.iterrows():
    # === ADD HEADER INFORMATION FOR THIS EVENT ===
    
    # Add the event number in the top right corner (Event 1, Event 2, etc.)
    event_number = Paragraph(f"Event {event_row['Event Number']}", event_number_style)
    story.append(event_number)  # Add this text to our PDF content
    story.append(Spacer(1, 3*mm))  # Add some vertical space (10 millimeters)
    event_time = Paragraph(f"Start Time: {event_row['Start Time']}", start_time_style)
    story.append(event_time)
    story.append(Spacer(1, 3*mm))  # Add some vertical space (10 millimeters)
    
    # Add the event name as a large, centered title (e.g., "100m Sprint")
    event_title = Paragraph(event_row['Event Name'], title_style)
    story.append(event_title)
    
    # Add the year level and gender as a subtitle (e.g., "Year 8, Boys")
    subtitle_text = f"{event_row['Year Level']}, {event_row['Gender']}"
    subtitle = Paragraph(subtitle_text, subtitle_style)
    story.append(subtitle)
    
    # === CREATE THE MAIN SCORING TABLE ===
    # This table is where officials will record the results of each event
    
    # Start with the header row that explains what each column is for
    table_data = [
        ['Position', 'Competitor ID', 'Time/Distance/Height']  # Column headers
    ]
    
    # Add four empty rows for recording 1st, 2nd, 3rd, and 4th place results
    positions = ['1st', '2nd', '3rd', '4th']  # The placing positions
    for position in positions:
        table_data.append([position, '', ''])  # Position filled in, other columns left blank for officials
    
    # Create the table and set the width of each column
    # [40mm for Position, 60mm for Competitor ID, 60mm for Time/Distance/Height]
    table = Table(table_data, colWidths=[40*mm, 60*mm, 60*mm])
    # === STYLE THE SCORING TABLE ===
    # Make the table look professional with colors, borders, and proper spacing
    table.setStyle(TableStyle([
        # Style the header row (Position, Competitor ID, Time/Distance/Height)
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Light grey background for headers
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),       # Black text for headers
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),              # Center all text in the table
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Bold font for headers
        ('FONTSIZE', (0, 0), (-1, 0), 12),                  # 12-point font size for headers
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),             # Extra space below header text
        
        # Style the data rows (1st, 2nd, 3rd, 4th place rows)
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),        # Regular font for data rows
        ('FONTSIZE', (0, 1), (-1, -1), 11),                 # 11-point font size for data
        ('GRID', (0, 0), (-1, -1), 1, colors.black),        # Black border lines around all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),             # Center text vertically in cells
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightblue]),  # Alternate white and light blue rows
        ('TOPPADDING', (0, 1), (-1, -1), 10),               # Space above text in data rows
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),            # Space below text in data rows
    ]))
    
    # Add the scoring table to our PDF page
    story.append(table)
    
    # === ADD THE HOUSE POINTS SECTION ===
    # Add extra space between the scoring table and the house points section
    story.append(Spacer(1, 20*mm))  # 20 millimeters of blank space
    
    # Add "House Points" as a title for the second table
    house_points_title = Paragraph("House Points", title_style)
    story.append(house_points_title)
    story.append(Spacer(1, 3*mm))  # 10 millimeters of space after the title
    
    # === CREATE THE HOUSE POINTS TABLE ===
    # This table allows officials to track participation or points for each house
    
    # Set up the table data with headers and four house rows
    house_data = [
        ['House', 'Number of Participants'],  # Column headers
        ['Oliphant', ''],  # Empty cell for officials to fill in
        ['Florey', ''],    # Empty cell for officials to fill in
        ['Cairns', ''],    # Empty cell for officials to fill in
        ['Mawson', '']     # Empty cell for officials to fill in
    ]
    
    # Create the table with column widths: 40mm for house names, 100mm for participant numbers
    house_table = Table(house_data, colWidths=[40*mm, 100*mm])
    # === STYLE THE HOUSE POINTS TABLE ===
    # Apply formatting and the distinctive house colors
    house_table.setStyle(TableStyle([
        # Style the header row (House, Number of Participants)
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),    # Light grey background for headers
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),         # Black text for headers
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                # Center all text
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),      # Bold font for headers
        ('FONTSIZE', (0, 0), (-1, 0), 12),                    # 12-point font for headers
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),               # Space below header text
        
        # Style all the data rows (standard formatting)
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),          # Regular font for house names
        ('FONTSIZE', (0, 1), (-1, -1), 11),                   # 11-point font size
        ('GRID', (0, 0), (-1, -1), 1, colors.black),          # Black border lines
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),               # Center text vertically
        ('TOPPADDING', (0, 1), (-1, -1), 10),                 # Space above text
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),              # Space below text
        
        # Apply distinctive background colors for each house
        ('BACKGROUND', (0, 1), (-1, 1), colors.lightblue),    # Oliphant house = Light Blue
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightyellow),  # Florey house = Light Yellow
        ('BACKGROUND', (0, 3), (-1, 3), colors.lightcoral),   # Cairns house = Light Red
        ('BACKGROUND', (0, 4), (-1, 4), colors.lightgreen),   # Mawson house = Light Green
    ]))
    
    # Add the house points table to our PDF page
    story.append(house_table)

    # Add a footer at the bottom of the page with instructions for officials
    footer_text = """Use this sheet to record results and house points for this event.<br/><br/>
        Place a line through the page if the Event is not run<br/><br/>
        Return ALL sheets to AbEd Room & ICT Team for scoring once event is complete"""
    footer = Paragraph(footer_text, footer_style)
    story.append(Spacer(1, 10*mm))  # Add some space before the footer
    story.append(footer)
    
    # === FINISH THIS EVENT'S PAGE ===
    # Add a page break after each event (except for the very last event)
    # This ensures each event gets its own page
    if index < len(event_list) - 1:  # type: ignore # If this is not the last event
        story.append(PageBreak())  # Start a new page for the next event

# === STEP 5: CREATE THE FINAL PDF FILE ===
# Take all the content we've built (story) and turn it into a PDF file
doc.build(story)

# === STEP 6: SHOW COMPLETION MESSAGE ===
# Let the user know the PDF was created successfully
print(f"PDF created successfully: {pdf_filename}")
print(f"Generated {len(event_list)} event sheets")

