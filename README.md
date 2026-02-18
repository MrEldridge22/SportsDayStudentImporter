# Sports Day Participant Management

A Python script designed to extract student details from Timetabling Solutions V10 Development files and generate participant lists for sports carnival management.

## Overview

This script processes student data from a Timetabling Solutions V10 Development file (.tfx) and generates two essential outputs for sports day management:

1. **CSV file** (`Participant ID Upload.csv`) - Formatted for upload to [Houseplay](https://www.houseplay.com.au), a sports carnival tracking website
2. **PDF file** (`Group_Rosters.pdf`) - Participant ID numbers organized by care groups for distribution to teachers

## Features

- Extracts student information from Timetabling Solutions V10 Development files
- Automatically generates unique competitor numbers based on year level
- Creates formatted CSV output for Houseplay import
- Generates professional PDF rosters organized by care groups
- Handles data cleaning and formatting automatically

## Prerequisites

### Student Data Requirements
Before running the script, ensure that:
- Your timetable development file is up to date
- **All students have a house assigned**
- **All students have a home group (care group) assigned**
- Students missing house or home group assignments may cause errors or be excluded

### File Requirements
- Place your Timetabling Solutions V10 Development file (`.tfx`) in the same directory as the script
- The file should follow the naming convention: `TTD_[YEAR]_S1.tfx` (e.g., `TTD_2026_S1.tfx`)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SportsDay
```

### 2. Create a Virtual Environment
```bash
# Create a new virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Required Libraries
```bash
# Upgrade pip to the latest version
python -m pip install --upgrade pip

# Install required packages from requirements.txt
pip install -r requirements.txt
```

## Usage

1. **Prepare your data file**:
   - Export your current timetable data from Timetabling Solutions V10
   - Save the `.tfx` file in the script directory with the naming format `TTD_[YEAR]_S1.tfx`

2. **Update the year variable** (if necessary):
   - Open `main.py`
   - Modify the `year` variable at the top of the script to match your current year

3. **Run the script**:
   ```bash
   python main.py
   ```

## Output Files

### 1. Participant ID Upload.csv
- **Purpose**: Upload to Houseplay for sports carnival tracking
- **Contents**: Student details with assigned competitor numbers
- **Columns**: First Name, Last Name, Student ID, Year, Gender, House, Group, Competitor Number

### 2. Group_Rosters.pdf
- **Purpose**: Distribution to care group teachers
- **Contents**: Participant ID numbers organized by care groups
- **Format**: Professional PDF with tables showing competitor numbers, names, and year levels

## Competitor Number System

The script automatically assigns unique competitor numbers based on year level:
- **Year 7**: 7001, 7002, 7003...
- **Year 8**: 8001, 8002, 8003...
- **Year 9**: 9001, 9002, 9003...
- **Year 10**: 1001, 1002, 1003...
- **Year 11**: 1500, 1501, 1502...
- **Year 12**: 2001, 2002, 2003...

Numbers are assigned sequentially based on sorted order (Year → Group → First Name).

## Dependencies

- **pandas**: Data manipulation and CSV output
- **reportlab**: PDF generation
- **numpy**: Numerical operations (pandas dependency)

See `requirements.txt` for complete version information.

## Troubleshooting

### Common Issues

1. **FileNotFoundError**: Ensure your `.tfx` file is in the correct directory and follows the naming convention
2. **Missing student data**: Check that all students have house and home group assignments in your timetable system
3. **Import errors**: Ensure all required libraries are installed using `pip install -r requirements.txt`

### Data Requirements
- Students without house assignments will need to be manually assigned before running the script
- Students without home group assignments may be excluded from group rosters

## Support

For issues related to:
- **Timetabling Solutions**: Contact your timetabling software provider
- **Houseplay**: Visit [www.houseplay.com.au](https://www.houseplay.com.au) for support documentation
- **This script**: Create an issue in this repository

## License

This project is provided as-is for educational and administrative use in school sports day management.