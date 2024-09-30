import pandas as pd
from gensim.models import Word2Vec
import pandas as pd
import re
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


# existing excel file
excel_path = 'clinic_prospect.xlsx'
sheet_name = 'original' 

# new sheet name
sheet = 'cleaned'

# columns you want to remove
columns_to_remove_name = ['Explanation (if No or Maybe)', 'Notes', 'Address Line 2', 'City', 'County', 'Sources/Where Found the Information', 'Role', 'Primary Contact Email', 'Contacted Via Email', 'EIN']  

# columns you want to have binary encodings of 
    # 0 -> empty 
    # 1 -> non-empty
columns_binary_encoding = ['Clinic Contact person', 'Email', 'Phone', 'Org Phone Number', 'Primary Contact Name'] 

# text columns with unknown values 
columns_string_empty = ['Clinic Name if Different', 'Address Line 1', 'Web Address']

# columns that need to be vectorized
columns_w2v = ['Org Name', 'Clinic Name if Different', 'Address Line 1', 'Web Address']

# vector size 
vec_size = 50

# False: if you only want to generate modes/word embeddings and don't care to save cleaned results
# True: if you want to save the cleaned results 
save_into_excel = True

# remove specific columns by name and index
def remove_columns(df, columns_to_remove_name):
    df.drop(df.columns[0], axis=1, errors='ignore', inplace=True) # this drops the nameless first column on the original spreadsheet (the initials)
    df.drop(columns=columns_to_remove_name, errors='ignore', inplace=True)
    return df

# create binary encodings for the 'Mobile Clinic' column specifically (target)
def transform_to_binary(text):
    lowercase_text = str(text).strip().lower()
    if lowercase_text == 'yes':
        return 1
    elif lowercase_text == 'no':
        return 0
    else:
        return pd.NA # will be dropped later

# make binary encodings of certain columns
def binary_encodings(df, columns_binary_encoding):
    for column in columns_binary_encoding: 
        df[column] = np.where(df[column].notna(), 1, 0)
    return df

# make one-hot encodings of states
def state_encoding(df):
    if 'State' in df.columns:
        df = pd.get_dummies(df, columns=['State'], dtype=int)
    return df

# reformat zips to be exactly 5 digits 
def format_zip(zip_code):
    if pd.isna(zip_code) or not zip_code:
        formatted_zip = 0
    else: 
        zip_str = str(zip_code)
        formatted_zip = zip_str[:5].zfill(5)
    return formatted_zip

def fill_empty_string_columns(df, columns_string_empty): 
    for column in columns_string_empty:
        df[column] = df[column].fillna("unknown")
    return df

def extract_words(text): 
    # convert the text to lowercase
    text = str(text).lower()
    # remove punctuation
    text = re.sub('[^a-zA-Z]', ' ', text)
    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    # remove digits and special characters
    text = re.sub("(\\d|\\W)+", " ", text)
    # tokenize into a list of words
    tokens = text.split()
    return tokens if tokens else ['unknown'] # ['words', 'like', 'this'] -> cells per column

def get_model(df, column_name):
    # save/checks models in separate folder! 
    model_path = f'w2v_models/{column_name}_model.model'
    if os.path.exists(model_path):
        model = Word2Vec.load(model_path)
    else:
        all_sentences = df[column_name].tolist()
        non_empty_sentences = [sentence for sentence in all_sentences if sentence != ['unknown']] # only train on values that exist in the original dataset!
        model = Word2Vec(sentences=non_empty_sentences, vector_size=vec_size, min_count=1)
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save(model_path)
    return model

# if there are multiple words, sum up the vectors for each word and create an avg vector
def average_vector(tokens, model):
    valid_tokens = []
    for word in tokens:
        if word in model.wv.key_to_index:
            valid_tokens.append(word)
    if not valid_tokens:
        return np.zeros(model.vector_size)
    
    vectors = [] 
    for token in valid_tokens:
        vectors.append(model.wv[token])
    
    vectors = np.array(vectors)
    avg_vector = np.mean(vectors, axis=0)
    return avg_vector

# creates separate columns for each value in the vector (number of columns depend on vector size)
def expand_vectors(df, column_name, vector_size):
    vector_df = pd.DataFrame(data=df[column_name].tolist(), columns=[f'{column_name}_dim_{i}' for i in range(vector_size)], index=df.index)
    return pd.concat([df.drop(columns=[column_name]), vector_df], axis=1)


df = pd.read_excel(excel_path, sheet_name=sheet_name)

df = remove_columns(df, columns_to_remove_name)
print(f"Finished removing the following columns: {columns_to_remove_name}\n")
df['Mobile Clinic'] = df['Mobile Clinic'].apply(transform_to_binary)
df = df.dropna(subset=['Mobile Clinic'])
print(f"Finished transforming target column to binary classification and removing uncertainties")
df = binary_encodings(df, columns_binary_encoding)
print(f"Finished creating binary encodings of the following columns: {columns_binary_encoding}\n")
df = state_encoding(df)
print(f"Finished creating one hot encoding of the states\n")
df = fill_empty_string_columns(df, columns_string_empty)
print(f"Finished filling empty cells with '0' in the following columns: {columns_string_empty}\n")
df['Zip'] = df['Zip'].apply(format_zip)
print(f"Finished modifying zip codes to standard 5-digit zip\n")

for c in columns_w2v:
    df[c] = df[c].apply(extract_words)
    model = get_model(df, c) 
    df[c] = df[c].apply(lambda vector: average_vector(vector, model)) 
    df = expand_vectors(df, c, vec_size)
    print(f"\nFinished extracting words, creating/loading a model, finding the averaged token vector, and separating each dimension into unique columns for all vectors in column name: {c}\n")

    # can check word embeddings if you'd like!
    # word_embeddings = {}
    # for word in model.wv.key_to_index:
    #     word_embeddings[word] = model.wv[word]
    # df_embeddings = pd.DataFrame.from_dict(word_embeddings, orient='index')
    # df_embeddings.reset_index(inplace=True)
    # df_embeddings.columns = ['word'] + [f'dim_{i}' for i in range(model.vector_size)]
    # df_embeddings.to_csv(f'word_embeddings/{c}_embeddings.csv', index=False)
df.drop(columns=columns_w2v, errors='ignore', inplace=True)

# adds sheet in the same excel file (overrides existing data if not new)
if save_into_excel: 
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet, index=False)
    print(f"\nFinished adding to the {sheet} sheet!")
