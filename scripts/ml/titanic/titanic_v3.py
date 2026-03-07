import numpy as np
import pandas as pd
import os

import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt

pio.templates
import plotly.offline as py

py.init_notebook_mode(connected=True)
plt.style.use("seaborn-notebook")

import seaborn as sns

import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output

for dirname, _, filenames in os.walk("./"):
    for filename in filenames:
        print(os.path.join(dirname, filename))

train_data = pd.read_csv("./train.csv")
train_data.head()

test_data = pd.read_csv("./test.csv")
test_data.head()

train = pd.read_csv("./train.csv")
test = pd.read_csv("./test.csv")
print("Train columns:", train.columns.tolist())
print("Test columns:", test.columns.tolist())

data = [train_data, test_data]
for dataset in data:
    mean = train_data["Age"].mean()
    std = test_data["Age"].std()
    is_null = dataset["Age"].isnull().sum()

    rand_age = np.random.randint(mean - std, mean + std, size=is_null)

    age_slice = dataset["Age"].copy()
    age_slice[np.isnan(age_slice)] = rand_age
    dataset["Age"] = age_slice
    dataset["Age"] = train_data["Age"].astype(int)

survived = "survived"
not_survived = "not survived"
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
women = train_data[train_data["Sex"] == "female"]
men = train_data[train_data["Sex"] == "male"]
ax = sns.distplot(
    women[women["Survived"] == 1].Age.dropna(),
    bins=18,
    label=survived,
    ax=axes[0],
    kde=False,
    color="green",
)
ax = sns.distplot(
    women[women["Survived"] == 0].Age.dropna(),
    bins=40,
    label=not_survived,
    ax=axes[0],
    kde=False,
    color="red",
)
ax.legend()
ax.set_title("Female")
ax = sns.distplot(
    men[men["Survived"] == 1].Age.dropna(),
    bins=18,
    label=survived,
    ax=axes[1],
    kde=False,
    color="green",
)
ax = sns.distplot(
    men[men["Survived"] == 0].Age.dropna(),
    bins=40,
    label=not_survived,
    ax=axes[1],
    kde=False,
    color="red",
)
ax.legend()
_ = ax.set_title("Male")

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Analysis of Iris data using scatter matrix"),
        dcc.Dropdown(id="dropdown", options=[], value=[], multi=True),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(Output("graph", "figure"), Input("dropdown", "value"))
def update_bar_chart(dims):
    # df = pd.read_csv('./train.csv')
    # fig = px.scatter_3d(df, x='PassengerId', y='Sex', z='Age', color='Age')

    df = pd.read_csv("./train.csv")

    for template in ["plotly"]:
        fig = px.scatter(
            df,
            x="PassengerId",
            y="Age",
            color="Survived",
            log_x=True,
            size_max=20,
            template=template,
            title="Which Age Survived?",
        )

    return fig


# app.run_server(debug=True)

sns.barplot(x="Pclass", y="Survived", data=train_data)

plt.rc("xtick", labelsize=14)
plt.rc("ytick", labelsize=14)

plt.figure()
fig = train_data.groupby("Survived")["Pclass"].plot.hist(histtype="bar", alpha=0.8)
plt.legend(("Died", "Survived"), fontsize=12)
plt.xlabel("Pclass", fontsize=18)
plt.show()
