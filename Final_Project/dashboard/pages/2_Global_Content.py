import streamlit as st
import plotly.express as px

from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Global Catalogue", layout="wide")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data()
filtered_df = apply_sidebar_filters(df)

st.title("🌍 Global Catalogue")

st.write(
    """
    Netflix sources content from many countries around the world.
    This page explores where titles come from and which genres are
    most common across the catalogue.
    """
)

st.divider()

# --------------------------------------------------
# Country Analysis
# --------------------------------------------------

country_df = filtered_df.copy()

country_df = country_df.dropna(subset=["country"])

country_df["country"] = country_df["country"].str.split(",")

country_df = country_df.explode("country")

country_df["country"] = country_df["country"].str.strip()

top_countries = (
    country_df["country"]
    .value_counts()
    .head(15)
    .index
)

country_counts = (
    country_df[
        country_df["country"].isin(top_countries)
    ]
    .groupby(["country", "type"])
    .size()
    .reset_index(name="Titles")
)

fig = px.bar(
    country_counts,
    x="country",
    y="Titles",
    color="type",
    barmode="group",
    title="Top Content Producing Countries",
    color_discrete_map={
        "Movie": "#1f77b4",
        "TV Show": "#ff7f0e"
    }
)

fig.update_layout(
    template="simple_white",
    title_x=0.5,
    xaxis_title="Country",
    yaxis_title="Titles",
    xaxis_tickangle=-40,
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("Insight"):

    st.write(
        """
        The United States contributes the largest number of titles,
        followed by countries such as India, the United Kingdom,
        Japan and South Korea. The results highlight Netflix's
        increasingly global content strategy.
        """
    )

st.divider()

# --------------------------------------------------
# Country Selector
# --------------------------------------------------

selected_country = st.selectbox(
    "Explore a country",
    sorted(country_df["country"].unique())
)

country_only = country_df[
    country_df["country"] == selected_country
]

metric1, metric2 = st.columns(2)

metric1.metric(
    "Titles",
    len(country_only)
)

metric2.metric(
    "Movies",
    (country_only["type"] == "Movie").sum()
)

st.divider()

# --------------------------------------------------
# Genre Analysis
# --------------------------------------------------

genre_df = country_only.copy()

genre_df["listed_in"] = genre_df["listed_in"].str.split(",")

genre_df = genre_df.explode("listed_in")

genre_df["listed_in"] = genre_df["listed_in"].str.strip()

genre_counts = (
    genre_df["listed_in"]
    .value_counts()
    .head(10)
    .reset_index()
)

genre_counts.columns = ["Genre", "Titles"]

fig2 = px.bar(
    genre_counts,
    x="Titles",
    y="Genre",
    orientation="h",
    text="Titles",
    title=f"Most Common Genres in {selected_country}"
)

fig2.update_traces(
    textposition="outside"
)

fig2.update_layout(
    template="simple_white",
    title_x=0.5,
    height=550,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

with st.expander("Insight"):

    st.write(
        f"""
        Selecting different countries reveals how Netflix's catalogue
        varies across regions. While some countries contribute mostly
        movies, others have stronger representation in TV Shows or
        particular genres, reflecting differences in local production
        and audience preferences.
        """
    )

st.divider()

# --------------------------------------------------
# Download
# --------------------------------------------------

st.download_button(
    label="📥 Download Filtered Dataset",
    data=country_only.to_csv(index=False),
    file_name=f"{selected_country}_netflix_titles.csv",
    mime="text/csv"
)