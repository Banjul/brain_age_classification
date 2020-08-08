import csv, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

demo_dir = os.path.join(ROOT_DIR,'demographic')
data_dir = os.path.join(ROOT_DIR,'data')
raw_data_dir = os.path.join(data_dir,'raw')

images = sorted([each for each in os.listdir(raw_data_dir) if not each.startswith('.')])

new_dir = os.path.join(demo_dir,'newIXI.csv')

with open(new_dir, 'rt') as infile:
    reader = csv.reader(infile)
    i = 0
    for row in reader:
        if row[0] == "IXI_ID":
            continue
        subjectId =row[0].zfill(3)
        image_name = images[i][3:6]
        if image_name == subjectId:
            i += 1
        else:
            i += 1
            print(image_name)
            break

print (len(images))

# df = pd.read_csv(this_dir)
#
# with open(this_dir, 'rt') as infile, open(new_dir, 'wt') as outfile:
#     reader = csv.reader(infile)
#     writer = csv.writer(outfile)
#     for row in reader:
#         if row[1] == "AGE":
#             writer.writerow(row)
#             continue
#         age = int(float(row[1]))
#         if age >= 50:
#             row[1] = 1
#             writer.writerow(row)
#         else:
#             row[1] = 0
#             writer.writerow(row)

# df_drop_col = df.drop(['HEIGHT', 'WEIGHT', 'ETHNIC_ID', 'MARITAL_ID', 'OCCUPATION_ID', 'QUALIFICATION_ID'
#                           , 'DOB', 'DATE_AVAILABLE', 'STUDY_DATE'], axis=1)
# df_drop_row = df_drop_col.drop()
# print(df_drop_col)
