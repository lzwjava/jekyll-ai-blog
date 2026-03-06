import numpy.ma as ma
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow import keras

from recsysNN_utils import *

pd.set_option("display.precision", 1)

top10_df = pd.read_csv("./data/content_top10_df.csv")
bygenre_df = pd.read_csv("./data/content_bygenre_df.csv")

(
    item_train,
    user_train,
    y_train,
    item_features,
    user_features,
    item_vecs,
    movie_dict,
    user_to_genre,
) = load_data()

num_user_features = user_train.shape[1] - 3
num_item_features = item_train.shape[1] - 1
uvs = 3
ivs = 3
u_s = 3
i_s = 1
print(f"Number of training vectors: {len(item_train)}")

pprint_train(user_train, user_features, uvs, u_s, maxcount=5)

pprint_train(item_train, item_features, ivs, i_s, maxcount=5, user=False)

print(f"y_train[:5]: {y_train[:5]}")

item_train_unscaled = item_train
user_train_unscaled = user_train
y_train_unscaled = y_train

scalerItem = StandardScaler()
scalerItem.fit(item_train)
item_train = scalerItem.transform(item_train)

scalerUser = StandardScaler()
scalerUser.fit(user_train)
user_train = scalerUser.transform(user_train)

scalerTarget = MinMaxScaler((-1, 1))
scalerTarget.fit(y_train.reshape(-1, 1))
y_train = scalerTarget.transform(y_train.reshape(-1, 1))

print(np.allclose(item_train_unscaled, scalerItem.inverse_transform(item_train)))
print(np.allclose(user_train_unscaled, scalerUser.inverse_transform(user_train)))

item_train, item_test = train_test_split(
    item_train, train_size=0.80, shuffle=True, random_state=1
)
user_train, user_test = train_test_split(
    user_train, train_size=0.80, shuffle=True, random_state=1
)
y_train, y_test = train_test_split(
    y_train, train_size=0.80, shuffle=True, random_state=1
)
print(f"movie/item training data shape: {item_train.shape}")
print(f"movie/item test data shape: {item_test.shape}")

pprint_train(user_train, user_features, uvs, u_s, maxcount=5)

num_outputs = 32
tf.random.set_seed(1)
user_NN = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(num_outputs),
    ]
)

item_NN = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(num_outputs),
    ]
)

input_user = tf.keras.layers.Input(shape=(num_user_features))
vu = user_NN(input_user)
vu = tf.linalg.l2_normalize(vu, axis=1)

input_item = tf.keras.layers.Input(shape=(num_item_features))
vm = item_NN(input_item)
vm = tf.linalg.l2_normalize(vm, axis=1)

output = tf.keras.layers.Dot(axes=1)([vu, vm])

model = tf.keras.Model([input_user, input_item], output)

model.summary()

from public_tests import *

test_tower(user_NN)
test_tower(item_NN)

tf.random.set_seed(1)
cost_fn = tf.keras.losses.MeanSquaredError()
opt = keras.optimizers.Adam(learning_rate=0.01)
model.compile(optimizer=opt, loss=cost_fn)

tf.random.set_seed(1)
model.fit([user_train[:, u_s:], item_train[:, i_s:]], y_train, epochs=5)

model.evaluate([user_test[:, u_s:], item_test[:, i_s:]], y_test)

new_user_id = 5000
new_rating_ave = 0.0
new_action = 0.0
new_adventure = 5.0
new_animation = 0.0
new_childrens = 0.0
new_comedy = 0.0
new_crime = 0.0
new_documentary = 0.0
new_drama = 0.0
new_fantasy = 5.0
new_horror = 0.0
new_mystery = 0.0
new_romance = 0.0
new_scifi = 0.0
new_thriller = 0.0
new_rating_count = 3

user_vec = np.array(
    [
        [
            new_user_id,
            new_rating_count,
            new_rating_ave,
            new_action,
            new_adventure,
            new_animation,
            new_childrens,
            new_comedy,
            new_crime,
            new_documentary,
            new_drama,
            new_fantasy,
            new_horror,
            new_mystery,
            new_romance,
            new_scifi,
            new_thriller,
        ]
    ]
)

user_vecs = gen_user_vecs(user_vec, len(item_vecs))

suser_vecs = scalerUser.transform(user_vecs)
sitem_vecs = scalerItem.transform(item_vecs)

y_p = model.predict([suser_vecs[:, u_s:], sitem_vecs[:, i_s:]])

y_pu = scalerTarget.inverse_transform(y_p)

sorted_index = np.argsort(-y_pu, axis=0).reshape(-1).tolist()
sorted_ypu = y_pu[sorted_index]
sorted_items = item_vecs[sorted_index]

print_pred_movies(sorted_ypu, sorted_items, movie_dict, maxcount=10)

uid = 2

user_vecs, y_vecs = get_user_vecs(uid, user_train_unscaled, item_vecs, user_to_genre)

suser_vecs = scalerUser.transform(user_vecs)
sitem_vecs = scalerItem.transform(item_vecs)

y_p = model.predict([suser_vecs[:, u_s:], sitem_vecs[:, i_s:]])

y_pu = scalerTarget.inverse_transform(y_p)

sorted_index = np.argsort(-y_pu, axis=0).reshape(-1).tolist()
sorted_ypu = y_pu[sorted_index]
sorted_items = item_vecs[sorted_index]
sorted_user = user_vecs[sorted_index]
sorted_y = y_vecs[sorted_index]

print_existing_user(
    sorted_ypu,
    sorted_y.reshape(-1, 1),
    sorted_user,
    sorted_items,
    ivs,
    uvs,
    movie_dict,
    maxcount=50,
)


def sq_dist(a, b):
    d = 0.0
    for i in range(len(a)):
        d += (a[i] - b[i]) ** 2
    return d


a1 = np.array([1.0, 2.0, 3.0])
b1 = np.array([1.0, 2.0, 3.0])
a2 = np.array([1.1, 2.1, 3.1])
b2 = np.array([1.0, 2.0, 3.0])
a3 = np.array([0, 1, 0])
b3 = np.array([1, 0, 0])
print(f"squared distance between a1 and b1: {sq_dist(a1, b1):0.3f}")
print(f"squared distance between a2 and b2: {sq_dist(a2, b2):0.3f}")
print(f"squared distance between a3 and b3: {sq_dist(a3, b3):0.3f}")

test_sq_dist(sq_dist)

input_item_m = tf.keras.layers.Input(shape=(num_item_features))
vm_m = item_NN(input_item_m)
vm_m = tf.linalg.l2_normalize(vm_m, axis=1)
model_m = tf.keras.Model(input_item_m, vm_m)
model_m.summary()

scaled_item_vecs = scalerItem.transform(item_vecs)
vms = model_m.predict(scaled_item_vecs[:, i_s:])
print(f"size of all predicted movie feature vectors: {vms.shape}")

count = 50
dim = len(vms)
dist = np.zeros((dim, dim))

for i in range(dim):
    for j in range(dim):
        dist[i, j] = sq_dist(vms[i, :], vms[j, :])

m_dist = ma.masked_array(dist, mask=np.identity(dist.shape[0]))

disp = [["movie1", "genres", "movie2", "genres"]]
for i in range(count):
    min_idx = np.argmin(m_dist[i])
    movie1_id = int(item_vecs[i, 0])
    movie2_id = int(item_vecs[min_idx, 0])
    disp.append(
        [
            movie_dict[movie1_id]["title"],
            movie_dict[movie1_id]["genres"],
            movie_dict[movie2_id]["title"],
            movie_dict[movie1_id]["genres"],
        ]
    )
table = tabulate.tabulate(disp, tablefmt="html", headers="firstrow")

file_path = "output_table.html"

with open(file_path, "w") as file:
    file.write(table)

print(f"HTML table saved to {file_path}")
