---
audio: false
generated: true
lang: en
layout: post
title: Combining Historical Data with LSTM
translated: false
type: note
---

Combining historical stock data from the TigerOpen API with an LSTM model for analysis is feasible and a common approach in financial time series prediction. The second script retrieves historical stock data (e.g., OHLCV bars), which can be used to construct a dataset for training an LSTM model similar to the one in the first script. Below, I outline how you can integrate these two, address potential challenges, and provide a high-level approach to analyze stock data using an LSTM.

### High-Level Approach to Combine the Two

1. **Retrieve Historical Data**:
   - Use the `get_history_data` function from the second script to fetch historical stock data (e.g., for symbol '00700' or others).
   - The data includes open, high, low, close prices, volume, and timestamps, which can be used as features for the LSTM.

2. **Preprocess Data for LSTM**:
   - Convert the historical data into a format suitable for the LSTM model. This involves:
     - Normalizing the data (e.g., scaling prices and volumes to [0, 1]).
     - Creating sequences of historical data (e.g., use the past 60 days to predict the next day's closing price).
     - Encoding features (e.g., close price, volume) into a tensor format compatible with the LSTM input.

3. **Adapt the LSTM Model**:
   - Modify the `Net` class from the first script to handle financial time series data instead of text sequences.
   - Adjust the input size to match the number of features (e.g., close price, volume, etc.) instead of `vocab_size`.
   - Update the output layer to predict a continuous value (e.g., next day's closing price) or a classification (e.g., price increase/decrease).

4. **Train the Model**:
   - Split the historical data into training, validation, and test sets.
   - Train the LSTM using the preprocessed data, similar to the training loop in the first script.
   - Use a loss function like Mean Squared Error (MSE) for regression tasks or Cross-Entropy Loss for classification.

5. **Analyze and Predict**:
   - Use the trained LSTM to predict future stock prices or trends based on recent historical data.
   - Visualize predictions alongside actual data using `matplotlib`.

6. **Integrate with Trading**:
   - Use predictions to inform trading decisions in the `place_order` function.
   - For example, place a buy order if the LSTM predicts a price increase above a threshold.

### Code Example: Combining Historical Data with LSTM

Below is a sample code snippet that integrates the two scripts, focusing on preprocessing historical data and adapting the LSTM for stock price prediction.

```python
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tigeropen.common.consts import Language, Market, BarPeriod, QuoteRight
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.common.util.signature_utils import read_private_key
import os
from datetime import datetime

# --- TigerOpen API Setup ---
def get_client_config(sandbox=False):
    client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
    client_config.private_key = read_private_key(os.environ.get('TIGER_PEM'))
    client_config.tiger_id = os.environ.get('TIGER_TIGER_ID')
    client_config.account = os.environ.get('TIGER_ACCOUNT')
    client_config.language = Language.zh_CN
    return client_config

def get_history_data(symbol='00700', period=BarPeriod.DAY, begin_time='2024-01-01', end_time=None, limit=100):
    client_config = get_client_config()
    quote_client = QuoteClient(client_config)
    if not end_time:
        end_time = datetime.now().strftime('%Y-%m-%d')
    bars_dict = quote_client.get_bars(
        symbols=[symbol], period=period, begin_time=begin_time, end_time=end_time, limit=limit, right=QuoteRight.BR
    )
    bars = bars_dict.get(symbol, [])
    return pd.DataFrame([{
        'time': bar.time,
        'open': bar.open,
        'high': bar.high,
        'low': bar.low,
        'close': bar.close,
        'volume': bar.volume
    } for bar in bars])

# --- LSTM Model ---
class StockLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=50, num_layers=1):
        super(StockLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, bidirectional=False)
        self.l_out = nn.Linear(in_features=hidden_size, out_features=1)  # Predict next close price

    def forward(self, x):
        x, (h, c) = self.lstm(x)
        x = x[:, -1, :]  # Take the last time step
        x = self.l_out(x)
        return x

# --- Data Preprocessing ---
def prepare_data(df, sequence_length=60, target_col='close'):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[[target_col]].values)

    X, y = [], []
    for i in range(len(scaled_data) - sequence_length):
        X.append(scaled_data[i:i + sequence_length])
        y.append(scaled_data[i + sequence_length])

    X = np.array(X)
    y = np.array(y)

    # Split into train and test
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    return torch.Tensor(X_train), torch.Tensor(y_train), torch.Tensor(X_test), torch.Tensor(y_test), scaler

# --- Training Loop ---
def train_model(model, X_train, y_train, X_test, y_test, num_epochs=50, lr=3e-4):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    training_loss, validation_loss = [], []

    for epoch in range(num_epochs):
        model.train()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        training_loss.append(loss.item())

        model.eval()
        with torch.no_grad():
            val_outputs = model(X_test)
            val_loss = criterion(val_outputs, y_test)
            validation_loss.append(val_loss.item())

        if epoch % 5 == 0:
            print(f'Epoch {epoch}, Training Loss: {training_loss[-1]:.4f}, Validation Loss: {validation_loss[-1]:.4f}')

    return training_loss, validation_loss

# --- Main Execution ---
if __name__ == '__main__':
    # Fetch historical data
    df = get_history_data(symbol='00700', limit=1000)

    # Prepare data
    sequence_length = 60
    X_train, y_train, X_test, y_test, scaler = prepare_data(df, sequence_length=sequence_length, target_col='close')

    # Initialize and train LSTM
    model = StockLSTM(input_size=1, hidden_size=50, num_layers=1)
    training_loss, validation_loss = train_model(model, X_train, y_train, X_test, y_test, num_epochs=50)

    # Plot training and validation loss
    plt.figure()
    plt.plot(training_loss, 'r', label='Training Loss')
    plt.plot(validation_loss, 'b', label='Validation Loss')
    plt.legend()
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.show()

    # Make predictions
    model.eval()
    with torch.no_grad():
        predicted = model(X_test).numpy()

    # Inverse transform predictions
    predicted = scaler.inverse_transform(predicted)
    y_test_actual = scaler.inverse_transform(y_test.numpy())

    # Plot predictions vs actual
    plt.figure()
    plt.plot(y_test_actual, 'b', label='Actual Close Price')
    plt.plot(predicted, 'r', label='Predicted Close Price')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.show()
```

### Key Modifications and Notes

1. **Data Retrieval**:
   - The `get_history_data` function is used to fetch historical stock data for a given symbol (e.g., '00700' for Tencent).
   - The data is converted into a pandas DataFrame for easy manipulation.

2. **Preprocessing**:
   - The data is normalized using `MinMaxScaler` to scale the closing prices to [0, 1].
   - Sequences of `sequence_length` (e.g., 60 days) are created to predict the next day's closing price.
   - The data is split into training (80%) and testing (20%) sets.

3. **LSTM Model**:
   - The `StockLSTM` class is adapted to handle a single feature (closing price) or multiple features (e.g., close, volume) by adjusting `input_size`.
   - The output layer predicts a single value (next day's closing price) using a linear layer.

4. **Training**:
   - The training loop uses MSE loss for regression, suitable for predicting continuous values like stock prices.
   - The model is evaluated on the test set to track validation loss.

5. **Visualization**:
   - Training and validation losses are plotted to assess model convergence.
   - Predicted vs. actual closing prices are plotted to evaluate model performance.

### Potential Challenges and Considerations

1. **Data Quality and Quantity**:
   - The amount of historical data (e.g., `limit=1000` bars) may be insufficient for robust LSTM training. Consider fetching more data or using a smaller `sequence_length`.
   - Stock data can be noisy, and LSTM models may struggle with long-term dependencies or sudden market shifts.

2. **Feature Engineering**:
   - The example uses only the closing price. Including additional features (e.g., volume, moving averages, technical indicators like RSI) can improve model performance.
   - Feature selection and preprocessing (e.g., handling missing data, outliers) are critical.

3. **Model Complexity**:
   - The LSTM architecture is simple (1 layer, 50 hidden units). For complex financial data, consider deeper models, dropout for regularization, or other architectures like GRU or Transformer.

4. **Overfitting**:
   - Monitor training vs. validation loss to detect overfitting. Add dropout or weight decay if necessary.

5. **Real-Time Integration**:
   - To use the model for real-time trading, fetch recent data, preprocess it, and feed it into the trained LSTM to generate predictions.
   - Combine predictions with a trading strategy (e.g., buy if predicted price > current price by X%).

6. **API Limitations**:
   - Ensure your TigerOpen API credentials are correctly set in environment variables (`TIGER_PEM`, `TIGER_TIGER_ID`, `TIGER_ACCOUNT`).
   - Be aware of API rate limits and data availability for certain symbols or time periods.

### Example Output

Assuming the code runs successfully, you might see:

- Console output showing training and validation loss per epoch (e.g., `Epoch 0, Training Loss: 0.1234, Validation Loss: 0.1345`).
- A plot of training and validation loss over epochs, indicating convergence.
- A plot comparing predicted vs. actual closing prices for the test set, showing how well the LSTM captures trends.

### Next Steps

- **Enhance Features**: Incorporate technical indicators (e.g., MACD, Bollinger Bands) or sentiment data from X posts (if available via search).
- **Backtesting**: Test the LSTM predictions in a simulated trading environment using historical data to evaluate profitability.
- **Trading Integration**: Use the `place_order` function to execute trades based on LSTM predictions, with proper risk management.
- **Hyperparameter Tuning**: Experiment with `sequence_length`, `hidden_size`, `num_layers`, and learning rate to optimize performance.

### Would It Work?

Yes, combining historical stock data with an LSTM for analysis is a viable approach, widely used in algorithmic trading. However, success depends on:

- Sufficient and clean data.
- Proper preprocessing and feature engineering.
- A well-tuned LSTM model.
- A robust trading strategy to act on predictions.

Financial markets are inherently noisy and influenced by external factors (e.g., news, macroeconomic events), so LSTM predictions should be used cautiously, ideally as part of a broader strategy with risk controls.

If you want to dive deeper into any part (e.g., adding features, backtesting, or real-time trading), let me know!
