import json
# from pypdf import PdfReader
import pandas as pd
import pathlib
import math

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
  'PS4': {
    'name': 'Program Session 4',
    'shortcode': 'PS4',
    'start_time': '12:00:00',
    'end_time': '12:55:00',
    'value': 8,
  },
  'PS5': {
    'name': 'Program Session 5',
    'shortcode': 'PS5',
    'start_time': '14:00:00',
    'end_time': '14:55:00',
    'value': 16,
  },
  'PSE': {
    'name': 'Evening',
    'shortcode': 'PSE',
    'start_time': '15:00:00',
    'end_time': '15:55:00',
    'value': 32,
  },
}

possible_sections = ['A','B','C','D','E']

# print(json.dumps(timeblocks, indent=4))
# df = pd.read_excel(r"/Users/lcotton/persona/scouts/troop1861/summer_camp_tool/2025_strake/CourseData.xlsx")
# df.fillna(None, inplace=True)
df = pd.read_excel(r"C:\Users\lcotton\personal\scouts\troop1861\summer_camp_tool\2025_strake\CourseData.xlsx", converters={'ClassNum':str})
# print(df)
classes = []
for idx, row in df.iterrows():
  # print(row)
  if pd.isna(row['Fee']):
    row['Fee'] = None
  course = {
    'ClassNum': row['ClassNum'],
    'Title': row['Title'].strip(),
    'Days': row['Days'],
    'Fee': row['Fee'],
    'AdditionalInfo': None,
    # 'AdditionalInfo2': None,
  }
  schedule = {}
  for d in ['PS1','PS2','PS3','PS4','PS5','PSE']:
    # print(row['Title'],row[d])
    # print(schedule.keys())
    if not pd.isna(row[d]):
      for e in row[d].split(','):
        # print(e)
        if e in possible_sections:
          if e in schedule.keys():
            schedule[e].append(d)
          else:
            schedule.update({e: [d]})
  # print(schedule)
  course['Sections'] = schedule

  if not pd.isnull(row['AdditionalInfo']):
    tmp_info = []
    for tmp in row['AdditionalInfo'].split(';'):
      # print(tmp)
      if len(tmp)>5:
        tmp_info.append(tmp.strip())
      # key, data = tmp.split(': ')
      # if key=='Min age':
      #   course['MinAge']=data
      # elif key=='Max age':
      #   course['MaxAge']=data
      # elif key=='Min rank':
      #   course['MinRank']=data
    course['AdditionalInfo'] = tmp_info
        
  classes.append(course)

# print(classes)
# print(json.dumps(classes,indent=4))
# exit()

output = {
  'SummerCamp': classes,
  'TimeBlocks': timeblocks,
}

json_putput = json.dumps(output, indent=4)
print(pathlib.Path.joinpath(pathlib.Path.cwd(), 'course_data.js'))
with open(pathlib.Path.joinpath(pathlib.Path.cwd(), 'course_data.js'), mode='w') as f:
  f.write(json_putput)

