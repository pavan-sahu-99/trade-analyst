import streamlit as st
from utils import Ch_oi_oi_spurt, most_active_contracts, secorials, sectorial_stock

st.set_page_config(page_title="Trade Analyst", layout="wide")
st.title("📈 Trade Analyst")
#
menu = st.sidebar.radio("Select Feature", ["Indices","Intraday Boost", "Market Pulse", "Most Active Contracts"])

# Optional Refresh Button
if st.button('🔄 Refresh Data'):
    st.rerun()

if menu == "Intraday Boost":
    st.subheader("🔥 OI Spurts in Derivatives")
    df = Ch_oi_oi_spurt.get_oi_spurts()
    st.dataframe(df)

elif menu == "Indices":
    st.subheader("💥 All Sectorial Index Data")
    df = secorials.sectorials()
    st.dataframe(df)

# Sectorial F&O Stocks Section
elif menu == "Market Pulse":
    st.subheader("🏢 Sectorial F&O Stocks")

    # Available sectors
    sector_indices = [
        "NIFTY AUTO", "NIFTY BANK", "NIFTY FINANCIAL SERVICES", "NIFTY FMCG",
        "NIFTY IT", "NIFTY MEDIA", "NIFTY METAL", "NIFTY PHARMA",
        "NIFTY PSU BANK", "NIFTY PRIVATE BANK", "NIFTY REALTY",
        "NIFTY HEALTHCARE INDEX", "NIFTY OIL & GAS"
    ]

    selected_sector = st.selectbox("Select Sector Index", sector_indices)

    df = sectorial_stock.get_sector_data(selected_sector)

    if df is not None and not df.empty:
        st.success(f"Showing F&O stocks in {selected_sector}")
        st.dataframe(df)
    else:
        st.warning(f"No F&O data found for {selected_sector}")

elif menu == "Most Active Contracts":
    st.subheader("💥 Most Active Equities")
    df = most_active_contracts.most_active_eq()
    st.dataframe(df)

#streamlit run app.py