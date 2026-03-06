import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

train_data = pd.read_csv("./train.csv")

print(train_data.head())

print("Number of Training Examples = {}".format(train_data.shape[0]))

print(train_data.info())


class Net(nn.Module):
    def __init__(self, in_features):
        super(Net, self).__init__()
        hidden_unit = 30
        self.layer1 = nn.Linear(in_features, hidden_unit)
        self.layer2 = nn.Linear(hidden_unit, 3)

    def forward(self, x):
        x = F.tanh(x)
        x = self.layer1(x)
        x = F.sigmoid(x)
        x = self.layer2(x)
        x = F.log_softmax(x, dim=-1)
        return x


def train(model: Net, optimizer: optim.Adam, train_loader: DataLoader):
    model.train()

    loss_fn = nn.NLLLoss(reduction="sum")

    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()

        outputs = model(data)

        loss = loss_fn(outputs, target)

        loss.backward()

        optimizer.step()


def validate(model: Net, test_loader: DataLoader):
    model.eval()

    total = 0
    log_loss = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)

            target_onehot = torch.zeros(target.size(0), 3)
            target_onehot.scatter_(1, target.view(-1, 1), 1)

            log_loss += torch.sum(output * target_onehot)

            total += len(data)

    log_loss = -1 / total * log_loss
    print(f"log_loss: {log_loss}")


def predict(model: Net, test_loader: DataLoader) -> list:
    model.eval()

    preds = torch.tensor([])
    with torch.no_grad():
        for data, _ in test_loader:
            output = model(data)

            preds = torch.concat((preds, torch.exp(output)), dim=0)

    preds = preds.permute(1, 0).detach().tolist()

    return preds


gb = train_data.groupby("Status")
print(gb)

print(gb.size())

print(gb.mean())

sgb = train_data.groupby("Edema")
print(sgb.size())


def preprocess_data(data: pd.DataFrame):
    sex_mapping = {"M": 0, "F": 1}
    data["Sex"] = data["Sex"].map(sex_mapping)

    data["Age"] = data["Age"] / 1000

    edema_mapping = {"N": 0, "S": 1, "Y": 2}
    data["Edema"] = data["Edema"].map(edema_mapping)

    bool_items = ["Ascites", "Hepatomegaly", "Spiders"]

    bool_mapping = {"Y": 1, "N": 0}

    for column in bool_items:
        data[column] = data[column].map(bool_mapping)

    return data


def preprocess_train_data(data: pd.DataFrame):
    preprocess_data(data)

    status_mapping = {"C": 0, "CL": 1, "D": 2}
    data["Status"] = data["Status"].map(status_mapping)

    return data


train_data = preprocess_train_data(train_data)

y = train_data["Status"]

# features = ['N_Days', 'Age', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema',
#             'Bilirubin', 'Cholesterol', 'Albumin', 'Copper', 'Alk_Phos', 'SGOT',
#             'Tryglicerides', 'Platelets', 'Prothrombin', 'Stage']

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
]

X = pd.get_dummies(train_data[features])

X = torch.tensor(X.values, dtype=torch.float32)
y = torch.tensor(y.values, dtype=torch.long)

nan_indices = torch.where(torch.isnan(X))

rows, cols = nan_indices

for i in range(len(rows)):
    print(f"NaN at row {rows[i]}, column {cols[i]}")

# y_onehot = torch.zeros(y.size(0), 3)
# y_onehot.scatter_(1, y.type(torch.long), 1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.05, random_state=42
)

batch_size = 30
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

model = Net(in_features=len(features))

epochs = 1000

optimizer = optim.Adam(model.parameters(), lr=1e-1)

test_dataset = TensorDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

for i in range(epochs):
    train(model, optimizer, train_loader)
    validate(model, test_loader)

test_data = pd.read_csv("./test.csv")
test_data = preprocess_data(test_data)

X_test = pd.get_dummies(test_data[features])

X_test = torch.tensor(X_test.values, dtype=torch.float32)

test_dataset = TensorDataset(X_test, torch.zeros(X_test.size(0)))
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

predictions = predict(model, test_loader)


def create_column(predictions, label):
    return [(2 / 3 if pred == label else 1 / 3) for pred in predictions]


output = pd.DataFrame(
    {
        "id": test_data["id"],
        "Status_C": predictions[0],
        "Status_CL": predictions[1],
        "Status_D": predictions[2],
    }
)

output.to_csv("submission.csv", index=False)
