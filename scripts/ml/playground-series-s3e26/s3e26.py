import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

train_data = pd.read_csv("./train.csv")

print(train_data.head())

print("Number of Training Examples = {}".format(train_data.shape[0]))

print(train_data.info())

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


def display_missing(df):
    for col in df.columns.tolist():
        print("{} column missing values: {}".format(col, df[col].isnull().sum()))
    print("\n")


display_missing(train_data)

# df_all_corr = df.corr().abs().unstack().sort_values(kind="quicksort", ascending=False).reset_index()
# df_all_corr.rename(columns={"level_0": "Feature 1", "level_1": "Feature 2", 0: 'Correlation Coefficient'}, inplace=True)
# df_all_corr[df_all_corr['Feature 1'] == 'Age']
# print(df_all_corr)

gb = train_data.groupby("Status")
print(gb)

# want to see the distribution of the Status column
print(gb.size())

# and calculate the mean of each column for each Status
print(gb.mean())

y = train_data["Status"]
# features = ['N_Days', 'Copper', 'Alk_Phos', 'SGOT', 'Tryglicerides']

features = [
    "N_Days",
    "Age",
    "Sex",
    "Ascites",
    "Hepatomegaly",
    "Spiders",
    "Edema",
    "Bilirubin",
    "Cholesterol",
    "Albumin",
    "Copper",
    "Alk_Phos",
    "SGOT",
    "Tryglicerides",
    "Platelets",
    "Prothrombin",
    "Stage",
]

X = pd.get_dummies(train_data[features])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.05, random_state=42
)

# model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=1)
model = RandomForestClassifier(
    criterion="gini",
    n_estimators=1100,
    max_depth=5,
    min_samples_split=4,
    min_samples_leaf=5,
    # max_features='auto',
    oob_score=True,
    random_state=42,
    n_jobs=-1,
    verbose=1,
)

model.fit(X_train, y_train)

predictions1 = model.predict(X_test)

m = len(y_test)

count = sum(1 for i in range(m) if y_test.iloc[i] == predictions1[i])

print(f"rate={count / m}")

test_data = pd.read_csv("./test.csv")
X_test = pd.get_dummies(test_data[features])
predictions = model.predict(X_test)


def create_column(predictions, label):
    return [(2 / 3 if pred == label else 1 / 3) for pred in predictions]


output = pd.DataFrame(
    {
        "id": test_data["id"],
        "Status_C": create_column(predictions, "C"),
        "Status_CL": create_column(predictions, "CL"),
        "Status_D": create_column(predictions, "D"),
    }
)

output.to_csv("submission.csv", index=False)
