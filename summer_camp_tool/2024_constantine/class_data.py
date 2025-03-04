import json
from pypdf import PdfReader
import pandas as pd
import pathlib

timeblocks = {
  'PS1': {
    'name': 'Program Session 1',
    'shortcode': 'PS1',
    'start_time': '09:00:00',
    'end_time': '09:55:00',
    'value': 1,
  },
  'PS2': {
    'name': 'Program Session 2',
    'shortcode': 'PS2',
    'start_time': '10:00:00',
    'end_time': '10:55:00',
    'value': 2,
  },
  'PS3': {
    'name': 'Program Session 3',
    'shortcode': 'PS3',
    'start_time': '11:00:00',
    'end_time': '11:55:00',
    'value': 4,
  },
  'PSA': {
    'name': 'Add-on Activity',
    'shortcode': 'PSA',
    'start_time': '15:00:00',
    'end_time': '15:55:00',
    'value': 8,
  },
  'PS4': {
    'name': 'Program Session 4',
    'shortcode': 'PS4',
    'start_time': '12:00:00',
    'end_time': '12:55:00',
    'value': 16,
  },
  'PS5': {
    'name': 'Program Session 5',
    'shortcode': 'PS5',
    'start_time': '14:00:00',
    'end_time': '14:55:00',
    'value': 32,
  },
}

possible_sections = ['A','B','C','D','E']

# print(json.dumps(timeblocks, indent=4))
df = pd.read_excel(r"/Users/lcotton/Documents/Scouts/2024_SummerCamp_Constantin/ClassGrid.xlsx")
# df.fillna(None, inplace=True)
# print(df)
classes = []
for idx, row in df.iterrows():
  # print(row)
  course = {
    'ClassNum': row['ClassNum'],
    'Title': row['Title'],
    'Days': row['Days'],
    'Fee': row['Fee'],
    'AdditionalInfo': row['AdditionalInfo'],
  }
  schedule = {}
  for d in ['PS1','PS2','PS3','PSA','PS4','PS5']:
    # print(row[d])
    # print(schedule.keys())
    if row[d] in possible_sections:
      if row[d] in schedule.keys():
        schedule[row[d]].append(d)
      else:
        schedule.update({row[d]: [d]})
  # print(schedule)
  course['Sections'] = schedule

  if not pd.isnull(row['AdditionalInfo']):
    for tmp in row['AdditionalInfo'].split(', '):
      # print(tmp)
      key, data = tmp.split(': ')
      if key=='Min age':
        course['MinAge']=data
      elif key=='Max age':
        course['MaxAge']=data
      elif key=='Min rank':
        course['MinRank']=data
        
  classes.append(course)

# print(classes)
# print(json.dumps(classes,indent=4))

output = {
  'SummerCamp': classes,
  'TimeBlocks': timeblocks,
}

json_putput = json.dumps(output, indent=4)
print(pathlib.Path.joinpath(pathlib.Path.cwd(), 'course_data.js'))
with open(pathlib.Path.joinpath(pathlib.Path.cwd(), 'course_data.js'), mode='w') as f:
  f.write(json_putput)

