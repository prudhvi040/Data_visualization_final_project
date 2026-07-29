import streamlit as st

from utils import load_data

st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

df = load_data()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("🎬 Netflix Dashboard")

st.sidebar.markdown(
"""
Explore how Netflix's catalogue has evolved over time using interactive visualizations.

Use the navigation menu above to switch between dashboard pages.
"""
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("Netflix Movies and TV Shows Dashboard")

st.markdown(
"""
This dashboard presents an interactive analysis of the **Netflix Movies and TV Shows**
dataset. The visualizations explore catalogue growth, content types,
countries, genres, audience ratings, movie runtimes, directors,
and release trends.
"""
)

st.divider()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

total_titles = len(df)

movies = (df["type"] == "Movie").sum()

tv = (df["type"] == "TV Show").sum()

countries = (
    df["country"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .nunique()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Titles", f"{total_titles:,}")
c2.metric("Movies", f"{movies:,}")
c3.metric("TV Shows", f"{tv:,}")
c4.metric("Countries", f"{countries}")

st.divider()

# ---------------------------------------------------
# Dataset Preview
# ---------------------------------------------------

with st.expander("Preview Dataset"):

    st.dataframe(
        df.head(15),
        use_container_width=True
    )

st.divider()

# ---------------------------------------------------
# About
# ---------------------------------------------------

st.subheader("Project Overview")

st.write(
"""
The goal of this project is to understand how Netflix's catalogue has changed
over time.

The dashboard follows the same analytical questions presented in the Jupyter
Notebook, allowing users to interactively explore the data through Plotly
visualizations.
"""
)

st.info(
"""
👈 Use the navigation menu in the sidebar to explore each section of the dashboard.
"""
)

st.divider()

st.caption(
    "Created by Prudhvi Sai • Data Visualization Final Project"
)