import pandas as pd

import seaborn as sns

sns.set(style="darkgrid")


import warnings

warnings.filterwarnings("ignore")

SEED = 42


def concat_df(train_data, test_data):
    return pd.concat([train_data, test_data], sort=True).reset_index(drop=True)


def divide_df(all_data):
    return all_data.loc[:890], all_data.loc[891:].drop(["Survived"], axis=1)


df_train = pd.read_csv("./train.csv")
df_test = pd.read_csv("./test.csv")
df_all = concat_df(df_train, df_test)

df_train.name = "Training Set"
df_test.name = "Test Set"
df_all.name = "All Set"

dfs = [df_train, df_test]

print("Number of Training Examples = {}".format(df_train.shape[0]))
print("Number of Test Examples = {}\n".format(df_test.shape[0]))
print("Training X Shape = {}".format(df_train.shape))
print("Training y Shape = {}\n".format(df_train["Survived"].shape[0]))
print("Test X Shape = {}".format(df_test.shape))
print("Test y Shape = {}\n".format(df_test.shape[0]))
print(df_train.columns)
print(df_test.columns)

print(df_train.info())
df_train.sample(3)


def display_missing(df):
    for col in df.columns.tolist():
        print("{} column missing values: {}".format(col, df[col].isnull().sum()))
    print("\n")


for df in dfs:
    print("{}".format(df.name))
    display_missing(df)

df_all_corr = (
    df_all.corr()
    .abs()
    .unstack()
    .sort_values(kind="quicksort", ascending=False)
    .reset_index()
)
df_all_corr.rename(
    columns={
        "level_0": "Feature 1",
        "level_1": "Feature 2",
        0: "Correlation Coefficient",
    },
    inplace=True,
)
df_all_corr[df_all_corr["Feature 1"] == "Age"]

age_by_pclass_sex = df_all.groupby(["Sex", "Pclass"]).median()["Age"]

for pclass in range(1, 4):
    for sex in ["female", "male"]:
        print(
            "Median age of Pclass {} {}s: {}".format(
                pclass, sex, age_by_pclass_sex[sex][pclass]
            )
        )
print("Median age of all passengers: {}".format(df_all["Age"].median()))

df_all["Age"] = df_all.groupby(["Sex", "Pclass"])["Age"].apply(
    lambda x: x.fillna(x.median())
)

print(df_all[df_all["Embarked"].isnull()])

print(df_all[df_all["Fare"].isnull()])

med_fare = df_all.groupby(["Pclass", "Parch", "SibSp"]).Fare.median()[3][0][0]
df_all["Fare"] = df_all["Fare"].fillna(med_fare)
