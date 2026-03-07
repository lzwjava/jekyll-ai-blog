import pandas as pd

pd.set_option("display.max_columns", 100)
import numpy as np

import warnings

warnings.filterwarnings("ignore")

from tqdm.notebook import tqdm


import matplotlib.pyplot as plt

plt.style.use("ggplot")
import seaborn as sns

from sklearn.preprocessing import (
    PowerTransformer,
)
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    cross_val_score,
)
from sklearn.metrics import (
    log_loss,
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    HistGradientBoostingClassifier,
    ExtraTreesClassifier,
)
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier


train = pd.read_csv("./train.csv")
test = pd.read_csv("./test.csv")
submission = pd.read_csv("./sample_submission.csv")

print("The dimension of the train dataset is:", train.shape)
print("The dimension of the test dataset is:", test.shape)

print(train.describe())

print(test.describe())

train["Status"].value_counts(normalize=True).plot(
    kind="bar", color=["steelblue", "orange", "green"]
)
plt.ylabel("Percentage")
# plt.show()

fig, axes = plt.subplots(1, 3, figsize=(20, 7))

sns.boxplot(ax=axes[0], data=train, x="Status", y="Age", hue="Status")
sns.boxplot(ax=axes[1], data=train, x="Status", y="Bilirubin", hue="Status")
sns.boxplot(ax=axes[2], data=train, x="Status", y="Cholesterol", hue="Status")

# plt.show()

fig, axes = plt.subplots(1, 3, figsize=(20, 7))

sns.boxplot(ax=axes[0], data=train, x="Status", y="Albumin", hue="Status")
sns.boxplot(ax=axes[1], data=train, x="Status", y="Copper", hue="Status")
sns.boxplot(ax=axes[2], data=train, x="Status", y="Alk_Phos", hue="Status")

fig, axes = plt.subplots(1, 3, figsize=(20, 7))

sns.boxplot(ax=axes[0], data=train, x="Status", y="SGOT", hue="Status")
sns.boxplot(ax=axes[1], data=train, x="Status", y="Tryglicerides", hue="Status")
sns.boxplot(ax=axes[2], data=train, x="Status", y="Platelets", hue="Status")

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

cmap = sns.diverging_palette(100, 7, s=75, l=40, n=5, center="light", as_cmap=True)

sns.heatmap(
    ax=axes[0],
    data=pd.crosstab(train["Stage"], train["Status"], normalize="index"),
    annot=True,
    cmap=cmap,
    fmt=".2f",
)
sns.heatmap(
    ax=axes[1],
    data=pd.crosstab(train["Drug"], train["Status"], normalize="index"),
    annot=True,
    cmap=cmap,
    fmt=".2f",
)

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

cmap = sns.diverging_palette(100, 7, s=75, l=40, n=5, center="light", as_cmap=True)

sns.heatmap(
    ax=axes[0],
    data=pd.crosstab(train["Sex"], train["Status"], normalize="index"),
    annot=True,
    cmap=cmap,
    fmt=".2f",
)
sns.heatmap(
    ax=axes[1],
    data=pd.crosstab(train["Ascites"], train["Status"], normalize="index"),
    annot=True,
    cmap=cmap,
    fmt=".2f",
)

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

cmap = sns.diverging_palette(100, 7, s=75, l=40, n=5, center="light", as_cmap=True)

sns.heatmap(
    ax=axes[0],
    data=pd.crosstab(train["Hepatomegaly"], train["Status"], normalize="index"),
    annot=True,
    cmap=cmap,
    fmt=".2f",
)
sns.heatmap(
    ax=axes[1],
    data=pd.crosstab(train["Spiders"], train["Status"], normalize="index"),
    annot=True,
    cmap=cmap,
    fmt=".2f",
)

sns.heatmap(
    data=pd.crosstab(train["Edema"], train["Status"], normalize="index"),
    annot=True,
    cmap=cmap,
    fmt=".2f",
)

train = train.drop(columns="id", axis=1)
train["generated"] = 1

test = test.drop(columns="id", axis=1)
test["generated"] = 1

train = pd.concat([train], axis=0).reset_index(drop=True)

X = train.drop(columns=["Edema", "Status"], axis=1)
X["Drug"] = X["Drug"].map({"D-penicillamine": 0, "Placebo": 1})
X["Sex"] = X["Sex"].map({"F": 0, "M": 1})
X["Ascites"] = X["Ascites"].map({"N": 0, "Y": 1})
X["Hepatomegaly"] = X["Hepatomegaly"].map({"N": 0, "Y": 1})
X["Spiders"] = X["Spiders"].map({"N": 0, "Y": 1})
X = pd.concat([X, pd.get_dummies(train["Edema"], drop_first=True, dtype=int)], axis=1)

Y = train["Status"].map({"C": 0, "CL": 1, "D": 2})

test_md = test.drop(columns=["Edema"], axis=1)
test_md["Drug"] = test_md["Drug"].map({"D-penicillamine": 0, "Placebo": 1})
test_md["Sex"] = test_md["Sex"].map({"F": 0, "M": 1})
test_md["Ascites"] = test_md["Ascites"].map({"N": 0, "Y": 1})
test_md["Hepatomegaly"] = test_md["Hepatomegaly"].map({"N": 0, "Y": 1})
test_md["Spiders"] = test_md["Spiders"].map({"N": 0, "Y": 1})
test_md = pd.concat(
    [test_md, pd.get_dummies(test["Edema"], drop_first=True, dtype=int)], axis=1
)

skf = RepeatedStratifiedKFold(n_splits=10, n_repeats=1, random_state=42)

logit_cv = cross_val_score(
    make_pipeline(
        PowerTransformer(), LogisticRegression(multi_class="ovr", max_iter=1000)
    ),
    X,
    Y,
    scoring="neg_log_loss",
    cv=skf,
    n_jobs=-1,
)

print(f"The 10-folds oof Log-Loss score is {-1 * logit_cv.mean()}")

RF_cv = cross_val_score(
    RandomForestClassifier(
        **{
            "n_estimators": 1000,
            "criterion": "log_loss",
            "max_depth": 14,
            "min_samples_split": 3,
            "min_samples_leaf": 1,
            "max_features": 4,
            "random_state": 1,
            "n_jobs": -1,
        }
    ),
    X,
    Y,
    scoring="neg_log_loss",
    cv=skf,
    n_jobs=-1,
)

print(f"The 10-folds oof Log-Loss score of the RF is {-1 * RF_cv.mean()}")

ET_cv = cross_val_score(
    ExtraTreesClassifier(
        criterion="log_loss",
        n_estimators=500,
        min_samples_leaf=3,
        max_depth=15,
        random_state=2,
    ),
    X,
    Y,
    scoring="neg_log_loss",
    cv=skf,
    n_jobs=-1,
)

print(f"The 10-folds oof Log-Loss score of the ET is {-1 * ET_cv.mean()}")

HB_cv = cross_val_score(
    HistGradientBoostingClassifier(
        **{
            "l2_regularization": 8.876168706639714,
            "early_stopping": False,
            "learning_rate": 0.009956485590638034,
            "max_iter": 500,
            "max_depth": 16,
            "max_bins": 255,
            "min_samples_leaf": 16,
            "max_leaf_nodes": 18,
            "random_state": 3,
        }
    ),
    X,
    Y,
    scoring="neg_log_loss",
    cv=skf,
    n_jobs=-1,
)

print(f"The average 10-folds oof Log-Loss score of the HG is {-1 * HB_cv.mean()}")

LGBM_cv = cross_val_score(
    LGBMClassifier(
        **{
            "n_estimators": 1000,
            "learning_rate": 0.013657589160895923,
            "max_depth": 17,
            "reg_alpha": 1.9791969860931342,
            "reg_lambda": 1.2857088172765347,
            "num_leaves": 37,
            "subsample": 0.6351453342675659,
            "colsample_bytree": 0.2644509924064132,
        }
    ),
    X,
    Y,
    scoring="neg_log_loss",
    cv=skf,
    n_jobs=-1,
)

print(
    f"The average 10-folds oof Log-Loss score of the LGBM model is {-1 * LGBM_cv.mean()}"
)

XGB_cv = cross_val_score(
    XGBClassifier(
        **{
            "max_depth": 7,
            "learning_rate": 0.03570188608151033,
            "n_estimators": 1000,
            "gamma": 0.6440001307764849,
            "min_child_weight": 2,
            "colsample_bytree": 0.27034458854562116,
            "subsample": 0.8435412915999765,
        }
    ),
    X,
    Y,
    scoring="neg_log_loss",
    cv=skf,
    n_jobs=-1,
)

print(
    f"The average 10-folds oof Log-Loss score of the XGBoost model is {-1 * XGB_cv.mean()}"
)

Cat_cv = cross_val_score(
    CatBoostClassifier(
        loss_function="MultiClass",
        iterations=2000,
        learning_rate=0.01,
        depth=8,
        verbose=False,
        task_type="CPU",
    ),
    X,
    Y,
    scoring="neg_log_loss",
    cv=skf,
    n_jobs=-1,
)

print(
    f"The average 10-folds oof Log-Loss score of the CatBoost model is {-1 * Cat_cv.mean()}"
)

model_performance = pd.DataFrame()
model_performance["Model"] = [
    "Logistic",
    "RF",
    "ET",
    "Hist",
    "LGBM",
    "XGBoost",
    "CatBoost",
]
model_performance["10-folds oof Log-Loss"] = [
    -1 * logit_cv.mean(),
    -1 * RF_cv.mean(),
    -1 * ET_cv.mean(),
    -1 * HB_cv.mean(),
    -1 * LGBM_cv.mean(),
    -1 * XGB_cv.mean(),
    -1 * Cat_cv.mean(),
]
print(
    f"The followig table shows the performance of the considered models: \n\n{model_performance}"
)

md1 = make_pipeline(
    PowerTransformer(), LogisticRegression(multi_class="ovr", max_iter=1000)
)

md2 = RandomForestClassifier(
    **{
        "n_estimators": 1000,
        "criterion": "log_loss",
        "max_depth": 14,
        "min_samples_split": 3,
        "min_samples_leaf": 1,
        "max_features": 4,
        "random_state": 1,
        "n_jobs": -1,
    }
)

md3 = ExtraTreesClassifier(
    criterion="log_loss",
    n_estimators=1000,
    min_samples_leaf=1,
    max_depth=15,
    random_state=2,
)

md4 = HistGradientBoostingClassifier(
    **{
        "l2_regularization": 8.876168706639714,
        "early_stopping": False,
        "learning_rate": 0.009956485590638034,
        "max_iter": 500,
        "max_depth": 16,
        "max_bins": 255,
        "min_samples_leaf": 16,
        "max_leaf_nodes": 18,
        "random_state": 3,
    }
)

md5 = LGBMClassifier(
    **{
        "n_estimators": 1000,
        "learning_rate": 0.013657589160895923,
        "max_depth": 17,
        "reg_alpha": 1.9791969860931342,
        "reg_lambda": 1.2857088172765347,
        "num_leaves": 37,
        "subsample": 0.6351453342675659,
        "colsample_bytree": 0.2644509924064132,
    }
)

md6 = XGBClassifier(
    **{
        "max_depth": 7,
        "learning_rate": 0.03570188608151033,
        "n_estimators": 1000,
        "gamma": 0.6440001307764849,
        "min_child_weight": 2,
        "colsample_bytree": 0.27034458854562116,
        "subsample": 0.8435412915999765,
    }
)

md7 = CatBoostClassifier(
    loss_function="MultiClass",
    iterations=2000,
    learning_rate=0.01,
    depth=8,
    verbose=False,
    task_type="CPU",
)

md4_pred, md5_pred, md6_pred = list(), list(), list()
Y_test_list = list()

for i, (train_idx, test_idx) in enumerate(skf.split(X, Y)):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    Y_train, Y_test = Y.iloc[train_idx], Y.iloc[test_idx]

    md4.fit(X_train, Y_train)
    md4_pred.append(md4.predict_proba(X_test))

    md5.fit(X_train, Y_train)
    md5_pred.append(md5.predict_proba(X_test))

    md6.fit(X_train, Y_train)
    md6_pred.append(md6.predict_proba(X_test))

    Y_test_list.append(Y_test)

w4_weights, w5_weights, w6_weights = list(), list(), list()
scores = list()

for i in tqdm(range(0, 3000)):
    w4 = np.random.random_sample(size=1)[0]
    w5 = np.random.random_sample(size=1)[0]
    w6 = np.random.random_sample(size=1)[0]

    w4_weights.append(w4)
    w5_weights.append(w5)
    w6_weights.append(w6)

    scores_in = list()

    for j in range(0, 10):
        pred = w4 * md4_pred[j] + w5 * md5_pred[j] + w6 * md6_pred[j]
        scores_in.append(log_loss(Y_test_list[j], pred))

    scores.append(np.mean(scores_in))

results = pd.DataFrame()
results["w_md4"] = w4_weights
results["w_md5"] = w5_weights
results["w_md6"] = w6_weights
results["score"] = scores
results = results.sort_values(by="score", ascending=True).reset_index(drop=True)
results.head(10)

md4_fit = md4.fit(X, Y)
md5_fit = md5.fit(X, Y)
md6_fit = md6.fit(X, Y)

ens = (
    results["w_md4"][0] * md4_fit.predict_proba(test_md)
    + results["w_md5"][0] * md5_fit.predict_proba(test_md)
    + results["w_md6"][0] * md6_fit.predict_proba(test_md)
)

ens = pd.DataFrame(ens)
ens = ens.div(ens.sum(axis=1), axis=0)

submission.loc[:, ["Status_C", "Status_CL", "Status_D"]] = ens.values
submission.head()

submission.to_csv("baseline_sub_1.csv", index=False)
