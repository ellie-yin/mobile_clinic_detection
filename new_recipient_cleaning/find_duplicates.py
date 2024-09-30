import pandas as pd
from fuzzywuzzy import fuzz

# calculates % of similarity, 0-1
def similar(a, b):
    return fuzz.ratio(a, b) / 100.0

# load orig excel with existing clinics
excel_file = '/clinic_prospect.xlsx' 
excel_data = pd.read_excel(excel_file, engine='openpyxl')

# load csv of new clinics
csv_file = '/new_recipients.csv'
csv_data = pd.read_csv(csv_file)

matched_entries = []

# for each excel row, see if there's a duplicate organization name in the new clinics
for index1, row1 in excel_data.iterrows():
    org_name1 = row1['Org Name']
    for index2, row2 in csv_data.iterrows():
        recipient_name2 = row2['Recipient']
        similarity_ratio = similar(str(org_name1).lower(), str(recipient_name2).lower())
        
        # can adjust similarity threshold as needed! 
        if similarity_ratio > 0.8:
            # adds entry if duplicate, drops it from csv if not
            matched_entries.append(row2.to_dict())
            csv_data = csv_data.drop(index2)

# convert duplicate list to dataframe
matched_df = pd.DataFrame(matched_entries)

# save duplicates entries to a new CSV file
matched_csv_path = '/repeat_recipients.csv'
matched_df.to_csv(matched_csv_path, index=False)

# updates new recipient list without duplicate entries
csv_data.to_csv(csv_file, index=False)

print(f"Matched entries saved to {matched_csv_path}")
