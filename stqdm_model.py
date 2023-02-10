def stqdm_model():

    # load your stock market data into the stocks array
    stocks = np.array([[100, 105, 102, 110], [90, 95, 92, 80], [80, 85, 82, 70], [70, 75, 72, 60]])

    timesteps = 3
    input_dim = 1
    num_samples = stocks.shape[0] - timesteps

    X = np.zeros((num_samples, timesteps, input_dim))
    y = np.zeros((num_samples, 1))

    def create_model():
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.LSTM(units=64, input_shape=(timesteps, input_dim)))
        model.add(tf.keras.layers.Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    for i in range(num_samples):
        X[i] = stocks[i:i+timesteps, :1]
        y[i] = stocks[i+timesteps, -1:]

        # load your time series data into the X and y arrays
        timesteps = X.shape[1]
        input_dim = X.shape[2]

    model = create_model()
    num_epochs = 100
    
    # tqdm progress bar for model training
    with stqdm(total=num_epochs) as pbar:
        for epoch in range(num_epochs):
            model.fit(X, y, epochs=1, verbose=0)
            pbar.update(1)