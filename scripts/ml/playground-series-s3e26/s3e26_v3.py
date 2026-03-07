import pandas as pd

import matplotlib.pyplot as plt

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

group_items = [
    "N_Days",
    "Age",
    "Sex",
    "Ascites",
    "Hepatomegaly",
    "Spiders",
    "Edema",
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


def groupby_status():
    for column in group_items:
        gb = train_data.groupby([column, "Status"]).size().unstack(fill_value=0)
        gb.plot(kind="bar", stacked=True)
        plt.xlabel(column)
        plt.ylabel("Count")
        plt.title(f"Distribution of Status by {column}")
        plt.legend(title="Status")
        plt.show()


for column in group_items:
    vc = pd.value_counts(train_data[column])
    vc.plot(kind="bar")
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.title(f"Distribution of {column}")
    # plt.show()
