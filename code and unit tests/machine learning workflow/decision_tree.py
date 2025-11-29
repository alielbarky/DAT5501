import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score


FILE_NAME = r"data\ObesityDataSet_raw_and_data_sinthetic.csv"
FEATURE_COLS = ['Age', 'FAF', 'TUE', 'FAVC', 'SMOKE'] #the columns with the factors we used to predict obesity
#faf is physical activity frequency, tue is time spent using technology devices, favc is frequency of consumption of high caloric food
TARGET_COL = 'NObeyesdad'
TEST_SIZE = 0.3
RANDOM_STATE = 42

# Load the dataset
df = pd.read_csv(FILE_NAME)

le = LabelEncoder()

#encode binary categorical features (FAVC, SMOKE)
df['FAVC_encoded'] = le.fit_transform(df['FAVC'])
df['SMOKE_encoded'] = le.fit_transform(df['SMOKE'])

#encode the multi-class target variable (NObeyesdad)
df['NObeyesdad_encoded'] = le.fit_transform(df[TARGET_COL])

#FEATURE SELECTION & DATA SPLIT

# Use the encoded versions of the categorical features
final_feature_cols = ['Age', 'FAF', 'TUE', 'FAVC_encoded', 'SMOKE_encoded']
target_encoded_col = 'NObeyesdad_encoded'

X = df[final_feature_cols]
y = df[target_encoded_col]

# Split the data into training and testing sets (stratified to maintain class proportions)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

#model training and perditcion

#Train the decision tree classifier
clf = DecisionTreeClassifier(random_state=RANDOM_STATE)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

#evaluation
report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
precision_weighted = report_dict['weighted avg']['precision']
recall_weighted = report_dict['weighted avg']['recall']
f1_weighted = report_dict['weighted avg']['f1-score']

#print results
print("Factors Used for Prediction (Features):")
print(FEATURE_COLS)
print()
print("Overall Model Performance Metrics (Weighted Averages):")
print(f"Precision: {precision_weighted:.4f}")
print(f"Recall: {recall_weighted:.4f}")
print(f"F1-Score: {f1_weighted:.4f}")