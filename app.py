import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("OHLC,Volume,RSI,MACD Chart")
#Load the sheet
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFH0Am4UhvY6KaiFZEw5QhAP17wUog-QwhFY70h5SCUEsA2ZX6ccfNZlvf3sNV-KF9dlbjdP_6xt51/pub?gid=1177240346&single=true&output=csv"
df = pd.read_csv(sheet_url)

# Convert date column
df['Date'] = pd.to_datetime(df['Date'])

# Optional: Sort by date just in case
df = df.sort_values('Date')


# Calculate EMA for different periods
df['EMA10'] = df['Close'].ewm(span=10).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()
df['EMA50'] = df['Close'].ewm(span=50).mean()
df['EMA100'] = df['Close'].ewm(span=100).mean()
df['EMA200'] = df['Close'].ewm(span=200).mean()

# Calculate RSI
delta = df['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df['RSI'] = 100 - (100 / (1 + rs))

# Calculate MACD and Signal Line
df['EMA12'] = df['Close'].ewm(span=12).mean()  # 12-period EMA
df['EMA26'] = df['Close'].ewm(span=26).mean()  # 26-period EMA
df['MACD'] = df['EMA12'] - df['EMA26']  # MACD Line
df['Signal'] = df['MACD'].ewm(span=9).mean()  # Signal Line
df['MACD_hist'] = df['MACD'] - df['Signal']  # MACD Histogram

# Create subplots: OHLC chart, RSI chart, MACD chart, and Volume chart
fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                    vertical_spacing=0.03, subplot_titles=('OHLC', 'RSI', 'MACD', 'Volume'),
                    row_width=[0.2, 0.2, 0.2, 0.2])

# Plot OHLC chart with Close price
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                             low=df['Low'], close=df['Close'], name="OHLC"),
              row=1, col=1)

# Plot Close price along with EMA lines on the OHLC chart
fig.add_trace(go.Scatter(x=df.index, y=df['EMA10'], mode='lines', name='EMA10', line=dict(color='red')),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], mode='lines', name='EMA20', line=dict(color='blue')),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], mode='lines', name='EMA50', line=dict(color='orange')),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['EMA100'], mode='lines', name='EMA100', line=dict(color='green')),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['EMA200'], mode='lines', name='EMA200', line=dict(color='magenta')),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='yellow')),
              row=1, col=1)

# Plot RSI chart
fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='orange')),
              row=2, col=1)
fig.add_hline(y=70, line=dict(color='red', dash='dash'), row=2, col=1)
fig.add_hline(y=30, line=dict(color='green', dash='dash'), row=2, col=1)

# Plot MACD chart
fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD', line=dict(color='blue')),
              row=3, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['Signal'], mode='lines', name='Signal', line=dict(color='red')),
              row=3, col=1)
fig.add_trace(go.Bar(x=df.index, y=df['MACD_hist'], name='MACD Histogram', marker=dict(color='green', opacity=0.4)),
              row=3, col=1)

# Plot Volume bar chart
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker=dict(color='rgba(0, 100, 255, 0.4)')),
              row=4, col=1)

# Update layout
fig.update_layout(
    xaxis_rangeslider_visible=False,
    title="TCS.NS with EMA, RSI, MACD, and Volume",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark"
)

st.plotly_chart(fig,use_container_width=True)
