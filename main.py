import pandas as pd
import json

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
                                        'Code': 'StudentID',
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

# Compute ParticipantID
# For Year 11, first should be 1500 (i.e., don't add the +1 effect): subtract 1 for Year 11 only
students_df['ParticipantID'] = (
    students_df['__base'] + students_df['__seq'] - (students_df['Year'] == 11).astype(int)
).astype('Int64')

# Clean up helper columns
students_df = students_df.drop(columns=['__base', '__seq'])

# Save back out for import into Scoring System.
students_df.to_csv('data_with_ids.csv', index=False)
# print(students_df)