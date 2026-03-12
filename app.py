
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Conflict Market Monitor", layout="wide")

st.title("🌍 Global Conflict Market Monitor")

tickers = {
    "Gold": "GC=F",
    "Crude Oil": "CL=F",
    "Nifty 50": "^NSEI",
    "S&P 500": "^GSPC",
    "VIX": "^VIX"
}

data = {}

for name, ticker in tickers.items():
    df = yf.download(ticker, period="3mo", interval="1d")
    df["Daily Change %"] = df["Close"].pct_change() * 100
    df["Weekly Change %"] = df["Close"].pct_change(5) * 100
    data[name] = df

st.subheader("Market Snapshot")

cols = st.columns(len(tickers))

for i, (name, df) in enumerate(data.items()):
    latest = df.iloc[-1]

    cols[i].metric(
        label=name,
        value=f"{latest['Close']:.2f}",
        delta=f"{latest['Daily Change %']:.2f}%"
    )

st.divider()

st.subheader("Market Trends")

for name, df in data.items():
    fig = px.line(df, y="Close", title=name)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Conflict Risk Signal")

gold = data["Gold"]["Daily Change %"].iloc[-1]
sp = data["S&P 500"]["Daily Change %"].iloc[-1]
vix = data["VIX"]["Daily Change %"].iloc[-1]

risk_score = gold + vix - sp

st.metric("Risk Score", f"{risk_score:.2f}")

if gold > 0 and sp < 0 and vix > 0:
    st.error("⚠️ RISK-OFF ENVIRONMENT DETECTED")
else:
    st.success("Markets relatively stable")

st.divider()

st.subheader("Market Correlation")

prices = pd.DataFrame({
    name: df["Close"]
    for name, df in data.items()
})

corr = prices.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu",
    title="Asset Correlation"
)

st.plotly_chart(fig, use_container_width=True)
