def inference_model(LSTM_cell, densor, n_x=90, n_a=64, Ty=100):
    x0 = Input(shape=(1, n_x))

    a0 = Input(shape=(n_a,), name="a0")
    c0 = Input(shape=(n_a,), name="c0")
    a = a0
    c = c0
    x = x0

    outputs = []

    for t in range(Ty):
        a, _, c = LSTM_cell(x, initial_state=[a, c])

        out = densor(a)

        outputs.append(out)

        x = RepeatVector(1)(out)

    inference_model = Model(inputs=[x0, a0, c0], outputs=outputs)

    return inference_model


inference_model = inference_model(LSTM_cell, densor)

x1 = np.zeros((1, 1, 90))
x1[:, :, 35] = 1
a1 = np.zeros((1, n_a))
c1 = np.zeros((1, n_a))
predicting = inference_model.predict([x1, a1, c1])

indices = np.argmax(predicting, axis=-1)
results = to_categorical(indices, num_classes=90)
