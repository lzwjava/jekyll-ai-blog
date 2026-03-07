import numpy as np
from pydub import AudioSegment
import random
from td_utils import *

x = graph_spectrogram("audio_examples/example_train.wav")

_, data = wavfile.read("audio_examples/example_train.wav")
print("Time steps in audio recording before spectrogram", data[:, 0].shape)
print("Time steps in input after spectrogram", x.shape)

Tx = 5511
n_freq = 101

Ty = 1375

activates, negatives, backgrounds = load_raw_audio("./raw_data/")

print(
    "background len should be 10,000, since it is a 10 sec clip\n"
    + str(len(backgrounds[0])),
    "\n",
)
print(
    "activate[0] len may be around 1000, since an `activate` audio clip is usually around 1 second (but varies a lot) \n"
    + str(len(activates[0])),
    "\n",
)
print(
    "activate[1] len: different `activate` clips can have different lengths\n"
    + str(len(activates[1])),
    "\n",
)


def get_random_time_segment(segment_ms):
    segment_start = np.random.randint(low=0, high=10000 - segment_ms)
    segment_end = segment_start + segment_ms - 1

    return (segment_start, segment_end)


def is_overlapping(segment_time, previous_segments):
    segment_start, segment_end = segment_time

    overlap = False

    for previous_start, previous_end in previous_segments:
        if segment_start <= previous_end and segment_end >= previous_start:
            overlap = True
            break

    return overlap


def is_overlapping_test(target):
    assert target((670, 1430), []) == False, "Overlap with an empty list must be False"
    assert target((500, 1000), [(100, 499), (1001, 1100)]) == False, (
        "Almost overlap, but still False"
    )
    assert target((750, 1250), [(100, 750), (1001, 1100)]) == True, (
        "Must overlap with the end of first segment"
    )
    assert target((750, 1250), [(300, 600), (1250, 1500)]) == True, (
        "Must overlap with the begining of second segment"
    )
    assert target((750, 1250), [(300, 600), (600, 1500), (1600, 1800)]) == True, (
        "Is contained in second segment"
    )
    assert target((800, 1100), [(300, 600), (900, 1000), (1600, 1800)]) == True, (
        "New segment contains the second segment"
    )

    print("\033[92m All tests passed!")


is_overlapping_test(is_overlapping)

overlap1 = is_overlapping((950, 1430), [(2000, 2550), (260, 949)])
overlap2 = is_overlapping((2305, 2950), [(824, 1532), (1900, 2305), (3424, 3656)])
print("Overlap 1 = ", overlap1)
print("Overlap 2 = ", overlap2)


def insert_audio_clip(background, audio_clip, previous_segments):
    segment_ms = len(audio_clip)

    segment_time = get_random_time_segment(segment_ms)

    retry = 5
    while is_overlapping(segment_time, previous_segments) and retry >= 0:
        segment_time = get_random_time_segment(segment_ms)
        retry = retry - 1

    if not is_overlapping(segment_time, previous_segments):
        previous_segments.append(segment_time)

        new_background = background.overlay(audio_clip, position=segment_time[0])
    else:
        new_background = background
        segment_time = (10000, 10000)

    return new_background, segment_time


def insert_audio_clip_test(target):
    np.random.seed(5)
    audio_clip, segment_time = target(backgrounds[0], activates[0], [(0, 4400)])
    duration = segment_time[1] - segment_time[0]
    assert segment_time[0] > 4400, (
        "Error: The audio clip is overlaping with the first segment"
    )
    assert duration + 1 == len(activates[0]), (
        "The segment length must match the audio clip length"
    )
    assert audio_clip != backgrounds[0], (
        "The audio clip must be different than the pure background"
    )
    assert segment_time == (
        7286,
        8201,
    ), f"Wrong segment. Expected: Expected: (7286, 8201) got:{segment_time}"

    audio_clip, segment_time = target(backgrounds[0], activates[0], [(0, 9999)])
    assert segment_time == (
        10000,
        10000,
    ), "Segment must match the out by max-retry mark"
    assert audio_clip == backgrounds[0], (
        "output audio clip must be exactly the same input background"
    )

    print("\033[92m All tests passed!")


np.random.seed(5)
audio_clip, segment_time = insert_audio_clip(
    backgrounds[0], activates[0], [(3790, 4400)]
)
audio_clip.export("insert_test.wav", format="wav")
print("Segment Time: ", segment_time)


def insert_ones(y, segment_end_ms):
    _, Ty = y.shape

    segment_end_y = int(segment_end_ms * Ty / 10000.0)

    if segment_end_y < Ty:
        for i in range(segment_end_y + 1, segment_end_y + 51):
            if i < Ty:
                y[0, i] = 1

    return y


def insert_ones_test(target):
    segment_end_y = random.randrange(0, Ty - 50)
    segment_end_ms = int(segment_end_y * 10000.4) / Ty
    arr1 = target(np.zeros((1, Ty)), segment_end_ms)

    assert type(arr1) == np.ndarray, "Wrong type. Output must be a numpy array"
    assert arr1.shape == (1, Ty), "Wrong shape. It must match the input shape"
    assert np.sum(arr1) == 50, "It must insert exactly 50 ones"
    assert arr1[0][segment_end_y - 1] == 0, f"Array at {segment_end_y - 1} must be 0"
    assert arr1[0][segment_end_y] == 0, f"Array at {segment_end_y} must be 0"
    assert arr1[0][segment_end_y + 1] == 1, f"Array at {segment_end_y + 1} must be 1"
    assert arr1[0][segment_end_y + 50] == 1, f"Array at {segment_end_y + 50} must be 1"
    assert arr1[0][segment_end_y + 51] == 0, f"Array at {segment_end_y + 51} must be 0"

    print("\033[92m All tests passed!")


insert_ones_test(insert_ones)

arr1 = insert_ones(np.zeros((1, Ty)), 9700)
plt.plot(insert_ones(arr1, 4251)[0, :])
print("sanity checks:", arr1[0][1333], arr1[0][634], arr1[0][635])


def create_training_example(background, activates, negatives, Ty):
    background = background - 20

    y = np.zeros((1, Ty))

    previous_segments = []

    number_of_activates = np.random.randint(0, 5)
    random_indices = np.random.randint(len(activates), size=number_of_activates)
    random_activates = [activates[i] for i in random_indices]

    for random_activate in random_activates:
        background, segment_time = insert_audio_clip(
            background, random_activate, previous_segments
        )

        segment_start, segment_end = segment_time

        y = insert_ones(y, segment_end)

    number_of_negatives = np.random.randint(0, 3)
    random_indices = np.random.randint(len(negatives), size=number_of_negatives)
    random_negatives = [negatives[i] for i in random_indices]

    for random_negative in random_negatives:
        background, _ = insert_audio_clip(
            background, random_negative, previous_segments
        )

    background = match_target_amplitude(background, -20.0)

    file_handle = background.export("train" + ".wav", format="wav")

    x = graph_spectrogram("train.wav")

    return x, y


def create_training_example_test(target):
    np.random.seed(18)
    x, y = target(backgrounds[0], activates, negatives, 1375)

    assert type(x) == np.ndarray, "Wrong type for x"
    assert type(y) == np.ndarray, "Wrong type for y"
    assert tuple(x.shape) == (101, 5511), "Wrong shape for x"
    assert tuple(y.shape) == (1, 1375), "Wrong shape for y"
    assert np.all(x > 0), "All x values must be higher than 0"
    assert np.all(y >= 0), "All y values must be higher or equal than 0"
    assert np.all(y <= 1), "All y values must be smaller or equal than 1"
    assert np.sum(y) >= 50, "It must contain at least one activate"
    assert np.sum(y) % 50 == 0, "Sum of activate marks must be a multiple of 50"
    assert np.isclose(np.linalg.norm(x), 39745552.52075), (
        "Spectrogram is wrong. Check the parameters passed to the insert_audio_clip function"
    )

    print("\033[92m All tests passed!")


np.random.seed(18)
x, y = create_training_example(backgrounds[0], activates, negatives, Ty)

plt.plot(y[0])

np.random.seed(4543)
nsamples = 32
X = []
Y = []
for i in range(0, nsamples):
    if i % 10 == 0:
        print(i)
    x, y = create_training_example(backgrounds[i % 2], activates, negatives, Ty)
    X.append(x.swapaxes(0, 1))
    Y.append(y.swapaxes(0, 1))
X = np.array(X)
Y = np.array(Y)

X_dev = np.load("./XY_dev/X_dev.npy")
Y_dev = np.load("./XY_dev/Y_dev.npy")

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Dense,
    Activation,
    Dropout,
    Input,
    TimeDistributed,
    Conv1D,
)
from tensorflow.keras.layers import GRU, BatchNormalization
from tensorflow.keras.optimizers import Adam


def modelf(input_shape):
    X_input = Input(shape=input_shape)

    X = Conv1D(filters=196, kernel_size=15, strides=4)(X_input)

    X = BatchNormalization()(X)

    X = Activation("relu")(X)

    X = Dropout(rate=0.8)(X)

    X = GRU(128, return_sequences=True)(X)

    X = Dropout(rate=0.8)(X)

    X = BatchNormalization()(X)

    X = GRU(128, return_sequences=True)(X)

    X = Dropout(rate=0.8)(X)

    X = BatchNormalization()(X)

    X = Dropout(rate=0.8)(X)

    X = TimeDistributed(Dense(1, activation="sigmoid"))(X)

    model = Model(inputs=X_input, outputs=X)

    return model


from test_utils import *


def modelf_test(target):
    Tx = 5511
    n_freq = 101
    model = target(input_shape=(Tx, n_freq))
    expected_model = [
        ["InputLayer", [(None, 5511, 101)], 0],
        [
            "Conv1D",
            (None, 1375, 196),
            297136,
            "valid",
            "linear",
            (4,),
            (15,),
            "GlorotUniform",
        ],
        ["BatchNormalization", (None, 1375, 196), 784],
        ["Activation", (None, 1375, 196), 0],
        ["Dropout", (None, 1375, 196), 0, 0.8],
        ["GRU", (None, 1375, 128), 125184, True],
        ["Dropout", (None, 1375, 128), 0, 0.8],
        ["BatchNormalization", (None, 1375, 128), 512],
        ["GRU", (None, 1375, 128), 99072, True],
        ["Dropout", (None, 1375, 128), 0, 0.8],
        ["BatchNormalization", (None, 1375, 128), 512],
        ["Dropout", (None, 1375, 128), 0, 0.8],
        ["TimeDistributed", (None, 1375, 1), 129, "sigmoid"],
    ]
    comparator(summary(model), expected_model)


modelf_test(modelf)

model = modelf(input_shape=(Tx, n_freq))

model.summary()

from tensorflow.keras.models import model_from_json

json_file = open("./models/model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("./models/model.h5")

model.layers[2].trainable = False
model.layers[7].trainable = False
model.layers[10].trainable = False

opt = Adam(lr=1e-6, beta_1=0.9, beta_2=0.999)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

model.fit(X, Y, batch_size=16, epochs=1)

(
    loss,
    acc,
) = model.evaluate(X_dev, Y_dev)
print("Dev set accuracy = ", acc)


def detect_triggerword(filename):
    plt.subplot(2, 1, 1)

    audio_clip = AudioSegment.from_wav(filename)
    audio_clip = match_target_amplitude(audio_clip, -20.0)
    file_handle = audio_clip.export("tmp.wav", format="wav")
    filename = "tmp.wav"

    x = graph_spectrogram(filename)

    x = x.swapaxes(0, 1)
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x)

    plt.subplot(2, 1, 2)
    plt.plot(predictions[0, :, 0])
    plt.ylabel("probability")
    plt.show()
    return predictions


chime_file = "audio_examples/chime.wav"


def chime_on_activate(filename, predictions, threshold):
    audio_clip = AudioSegment.from_wav(filename)
    chime = AudioSegment.from_wav(chime_file)
    Ty = predictions.shape[1]

    consecutive_timesteps = 0
    i = 0

    while i < Ty:
        consecutive_timesteps += 1

        if consecutive_timesteps > 20:
            audio_clip = audio_clip.overlay(
                chime, position=((i / Ty) * audio_clip.duration_seconds) * 1000
            )

            consecutive_timesteps = 0
            i = 75 * (i // 75 + 1)
            continue

        if predictions[0, i, 0] < threshold:
            consecutive_timesteps = 0
        i += 1

    audio_clip.export("chime_output.wav", format="wav")


filename = "./raw_data/dev/1.wav"
prediction = detect_triggerword(filename)
chime_on_activate(filename, prediction, 0.5)

filename = "./raw_data/dev/2.wav"
prediction = detect_triggerword(filename)
chime_on_activate(filename, prediction, 0.5)


def preprocess_audio(filename):
    padding = AudioSegment.silent(duration=10000)
    segment = AudioSegment.from_wav(filename)[:10000]
    segment = padding.overlay(segment)

    segment = segment.set_frame_rate(44100)

    segment.export(filename, format="wav")


your_filename = "audio_examples/my_audio.wav"

preprocess_audio(your_filename)

chime_threshold = 0.5
prediction = detect_triggerword(your_filename)
chime_on_activate(your_filename, prediction, chime_threshold)
