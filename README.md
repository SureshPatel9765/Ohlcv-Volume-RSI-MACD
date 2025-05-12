# Ohlcv-Volume-RSI-MACD
Google Sheet and Python combination for technical chart
# OHLCV + Volume + RSI + MACD Streamlit App

This app displays stock charts using data from **Google Sheets**, including:

- **Candlestick (OHLC)** chart
- **Volume** (non-negative, auto-scaled)
- **RSI (Relative Strength Index)**
- **MACD** with Signal Line and Histogram

No `yfinance` used — 

1. Data is pulled into Google Sheets using:
   ```excel
   =GOOGLEFINANCE("TCS.NS", "all", TODAY()-180, TODAY(), "DAILY")
2. The Streamlit app reads that data using gspread.

3. Plots are generated using Plotly.
   
Requirements
____________


streamlit
plotly
pandas
gspread
oauth2client

Run locally
___________

git clone https://github.com/SureshPatel9765/Ohlcv-Volume-RSI-MACD.git
cd Ohlcv-Volume-RSI-MACD
pip install -r requirements.txt
streamlit run app.py

License
_______

Free to use for personal or academic purposes.







