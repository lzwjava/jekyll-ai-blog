import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

for dirname, _, filenames in os.walk("./"):
    for filename in filenames:
        print(os.path.join(dirname, filename))

train_data = pd.read_csv("./train.csv")
test_data = pd.read_csv("./test.csv")

print(train_data.head())

y = train_data["Survived"]
features = ["Age", "Pclass", "Sex", "SibSp", "Parch", "Fare"]

train_data["Age"].fillna(0, inplace=True)
test_data["Age"].fillna(0, inplace=True)

train_data["Fare"].fillna(0, inplace=True)
test_data["Fare"].fillna(0, inplace=True)

X = pd.get_dummies(train_data[features])
print(X)

X_test = pd.get_dummies(test_data[features])

model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=10)
model.fit(X, y)

predictions1 = model.predict(X)

m = len(y)

count = 0

for i in range(m):
    if y[i] == predictions1[i]:
        count += 1

print(f"rate={count / m}")

predictions = model.predict(X_test)

output = pd.DataFrame({"PassengerId": test_data.PassengerId, "Survived": predictions})
output.to_csv("submission.csv", index=False)

print("submitted")
