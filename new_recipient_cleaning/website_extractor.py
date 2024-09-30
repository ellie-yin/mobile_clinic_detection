import pandas as pd
from googlesearch import search
import ssl

# disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

file_path = '/recipients_without_emails.csv'
data = pd.read_csv(file_path)

# finds website based on the name, city, and state of the recipient: ex. Blue Cross Cambridge MA
def find_website(row):
    query = f"{row['Recipient']} {row['City']} {row['State']}"
    try:
        for url in search(query, num=1, stop=1, pause=2):
            return url
    except Exception as e: # uf you can't find something, it prints an error and doesn't return anything --> blank
        print(f"Exception occurred for {query}: {e}")
        return None
    
# creates a website column and applies it to each of the rows
data['Website'] = data.apply(find_website, axis=1)

# add the data to a new csv 
updated_file_path = '/recipients_with_websites.csv'
data.to_csv(updated_file_path, index=False)

print(f"Updated file saved to {updated_file_path}")
