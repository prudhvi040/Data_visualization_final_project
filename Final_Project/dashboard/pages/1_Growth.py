import streamlit as st
import plotly.express as px

from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Growth & Expansion", layout="wide")

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

df = load_data()
filtered_df = apply_sidebar_filters(df)

st.title("📈 Growth & Expansion")

st.write(
    """
    This section explores how Netflix's catalogue has expanded over time
    and how the balance between Movies and TV Shows has evolved.
    """
)

st.divider()

# -----------------------------------------------------
# KPI Cards
# -----------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Filtered Titles",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Movies",
    f"{(filtered_df['type'] == 'Movie').sum():,}"
)

col3.metric(
    "TV Shows",
    f"{(filtered_df['type'] == 'TV Show').sum():,}"
)

st.divider()

# -----------------------------------------------------
# Chart 1
# Catalogue Growth
# -----------------------------------------------------

yearly = (
    filtered_df
    .groupby("added_year")
    .size()
    .reset_index(name="Titles Added")
)

fig = px.line(
    yearly,
    x="added_year",
    y="Titles Added",
    markers=True,
    title="Catalogue Growth Over Time"
)

fig.update_traces(line=dict(width=3))

fig.update_layout(
    template="simple_white",
    title_x=0.5,
    xaxis_title="Year Added",
    yaxis_title="Number of Titles",
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("Insight"):

    st.write(
        """
        Netflix's catalogue expanded rapidly between 2016 and 2019.
        After this period, the number of new titles added each year
        became more stable. This suggests that Netflix shifted from
        rapid catalogue expansion to maintaining a large and diverse
        content library.
        """
    )

st.divider()

# -----------------------------------------------------
# Chart 2
# Movies vs TV Shows
# -----------------------------------------------------

type_year = (
    filtered_df
    .groupby(["added_year", "type"])
    .size()
    .reset_index(name="Count")
)

fig2 = px.line(
    type_year,
    x="added_year",
    y="Count",
    color="type",
    markers=True,
    color_discrete_map={
        "Movie": "#1f77b4",
        "TV Show": "#ff7f0e"
    },
    title="Movies vs TV Shows Added Over Time"
)

fig2.update_layout(
    template="simple_white",
    title_x=0.5,
    xaxis_title="Year Added",
    yaxis_title="Number of Titles",
    legend_title="Content Type",
    height=550
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

with st.expander("Insight"):

    st.write(
        """
        Movies have consistently represented a large share of Netflix's
        catalogue. However, the number of TV Shows added each year
        increased significantly after 2015, reflecting Netflix's
        growing investment in original series and episodic content.
        """
    )

st.divider()

# -----------------------------------------------------
# Download
# -----------------------------------------------------

st.download_button(
    label="📥 Download Filtered Dataset",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_netflix_growth.csv",
    mime="text/csv"
)