import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# LOAD CUSTOM DATASET
excel_path = 'clinic_prospect.xlsx'
sheet = 'cleaned'

df = pd.read_excel(excel_path, sheet_name=sheet)

# DATA PREPROCESSING
# already took care of preprocessing in the cleaning script
# split data into features (X) and target (y): 
X = df.drop(columns=['Mobile Clinic'], axis=1).values  
y = df['Mobile Clinic'].values
# convert dataframe to pytorch tensors
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32) 

# SPLIT INTO TRAIN AND TEST SETS
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# MODEL TRAINING 
model = LogisticRegression(max_iter=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# ACCURACY 
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
# Accuracy: 0.89
