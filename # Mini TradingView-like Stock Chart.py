# Mini TradingView-like Stock Chart Viewer using Streamlit
# This app allows users to input a stock symbol and view an interactive candlestick chart.
# Requirements:
# - Install necessary libraries: pip install streamlit yfinance plotly
# - Run the app: streamlit run this_script.py

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit page configuration
st.set_page_config(page_title="Mini TradingView", layout="wide")

# Sidebar for user inputs
st.sidebar.header("Stock Chart Settings")
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL)", value="AAPL").upper()
period = st.sidebar.selectbox("Select Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], index=5)
interval = st.sidebar.selectbox("Select Interval", ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"], index=8)

# Fetch stock data
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_stock_data(symbol, period, interval):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period, interval=interval)
        if data.empty:
            st.error("No data found for the given symbol.")
            return None
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

data = fetch_stock_data(symbol, period, interval)

# Main content
st.title(f"Stock Chart for {symbol}")

if data is not None:
    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'],
                                         name=symbol)])
    
    # Add volume bar chart
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', yaxis='y2', opacity=0.3))
    
    # Update layout for better visuals
    fig.update_layout(
        title=f"{symbol} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False),
        xaxis_rangeslider_visible=True,
        height=600,
        template="plotly_dark"  # Dark theme like TradingView
    )
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Display basic stock info
    st.subheader("Stock Information")
    stock = yf.Ticker(symbol)
    info = stock.info
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
    with col2:
        st.write(f"**Current Price:** ${info.get('currentPrice', 'N/A')}")
        st.write(f"**Market Cap:** ${info.get('marketCap', 'N/A'):,}")
        st.write(f"**52-Week High:** ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.write(f"**52-Week Low:** ${info.get('fiftyTwoWeekLow', 'N/A')}")

    # Display raw data table
    st.subheader("Raw Data")
    st.dataframe(data.tail(10))  # Show last 10 rows

else:
    st.info("Enter a valid stock symbol to view the chart.")