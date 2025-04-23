import streamlit as st
from utils import Ch_oi_oi_spurt, most_active_contracts, secorials, sectorial_stock
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Trade Analyst", layout="wide")
st.title("📈 Trade Analyst")
#
menu = st.sidebar.radio("Select Feature", ["Indices","Overview","Intraday Boost", "Market Pulse", "Most Active Contracts"])

# Optional Refresh Button
if st.button('🔄 Refresh Data'):
    st.rerun()

if menu == "Intraday Boost":
    st.subheader("🔥 OI Spurts in Derivatives")
    df = Ch_oi_oi_spurt.get_oi_spurts()
    st.dataframe(df)

elif menu == "Overview":
    st.subheader("🔥 Nifty 50 Heat Map")
    df = sectorial_stock.get_sector_data("NIFTY 50")
    df_sorted = df.sort_values(by="% Change", ascending=False).reset_index(drop=True)
    df_sorted['Row'] = df_sorted.index // 10
    df_sorted['Col'] = df_sorted.index % 10

    fig = px.imshow(
         df_sorted.pivot(index="Row", columns="Col", values="% Change"),
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        aspect="auto"
        )

    for i, row in df_sorted.iterrows():
        value = row["% Change"]
        symbol = row["Symbol"]
        fig.add_annotation(
            text=f"{symbol}<br>{value:.2f}%",
            x=row['Col'],
            y=row['Row'],
            showarrow=False,
            font=dict(size=10, color="black"),
            align="center"
        )
    fig.update_layout(
       title="Nifty 50 Heatmap by % Change",
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        height=600,
        margin=dict(l=20, r=20, t=60, b=20)
        )

    st.plotly_chart(fig, use_container_width=True)
    

elif menu == "Indices":
    st.subheader("💥 All Sectorial Index Data")
    df = secorials.sectorials()
    st.dataframe(df)

    if "% Change" in df.columns:
        df_sort = df.sort_values(by="% Change",ascending=False)

        fig = px.bar(
            df_sort,
            x="Index",
            y="% Change",
            orientation="v",  # vertical bars
            color="% Change",
            color_continuous_scale=[(0.0, "red"), (0.5, "lightblue"), (1.0, "blue")],
            title="📊 Sectorial Performance",
        )

        fig.update_layout(
            plot_bgcolor="#000000",  # black plot background
            paper_bgcolor="#000000",  # black outer background
            font=dict(color="#FFFFFF"),  # white font
            xaxis=dict(title="Index", color="#FFFFFF", tickangle=-45),
            yaxis=dict(title="% Change", color="#FFFFFF"),
        )

        fig.update_traces(
            marker_line_color='#FFFFFF',  # white outline
            marker_line_width=1,
            hovertemplate='%{x}: %{y:.2f}%'
        )

        st.plotly_chart(fig, use_container_width=True)


        

# Sectorial F&O Stocks Section
elif menu == "Market Pulse":
    st.subheader("🏢 Sectorial F&O Stocks")

    # Available sectors
    sector_indices = [
        "NIFTY AUTO", "NIFTY BANK", "NIFTY FINANCIAL SERVICES", "NIFTY FMCG",
        "NIFTY IT", "NIFTY MEDIA", "NIFTY METAL", "NIFTY PHARMA",
        "NIFTY PSU BANK", "NIFTY PRIVATE BANK", "NIFTY REALTY",
        "NIFTY HEALTHCARE INDEX", "NIFTY OIL & GAS","NIFTY 50"
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

# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# .\.venv\Scripts\activate
#streamlit run app.py