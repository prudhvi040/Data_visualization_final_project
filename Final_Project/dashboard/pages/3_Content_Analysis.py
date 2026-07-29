import streamlit as st
import plotly.express as px

from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Content Insights", layout="wide")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data()
filtered_df = apply_sidebar_filters(df)

st.title("🎬 Content Insights")

st.write(
    """
    This section explores Netflix's audience ratings, movie runtimes,
    and the directors who appear most frequently in the catalogue.
    """
)

st.divider()

# ==================================================
# Ratings
# ==================================================

rating_counts = (
    filtered_df
    .groupby(["rating", "type"])
    .size()
    .reset_index(name="Titles")
)

fig = px.bar(
    rating_counts,
    x="rating",
    y="Titles",
    color="type",
    barmode="group",
    title="Audience Ratings by Content Type",
    color_discrete_map={
        "Movie": "#1f77b4",
        "TV Show": "#ff7f0e"
    }
)

fig.update_layout(
    template="simple_white",
    title_x=0.5,
    xaxis_title="Rating",
    yaxis_title="Number of Titles",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Insight"):
    st.write(
        """
        Mature audience ratings such as TV-MA and TV-14 account for a
        large share of Netflix's catalogue. Movies cover a wider range
        of ratings, while TV Shows are concentrated in a smaller number
        of audience categories.
        """
    )

st.divider()

# ==================================================
# Runtime Explorer
# ==================================================

movie_df = filtered_df[
    (filtered_df["type"] == "Movie") &
    (filtered_df["duration_num"].notna()) &
    (filtered_df["rating"].notna())
]

ratings = sorted(movie_df["rating"].unique())

selected_rating = st.selectbox(
    "Choose an audience rating",
    ratings
)

runtime_df = movie_df[
    movie_df["rating"] == selected_rating
]

col1, col2 = st.columns(2)

col1.metric(
    "Movies",
    len(runtime_df)
)

col2.metric(
    "Average Runtime",
    f"{runtime_df['duration_num'].mean():.1f} min"
)

fig2 = px.histogram(
    runtime_df,
    x="duration_num",
    nbins=20,
    title=f"Runtime Distribution for {selected_rating} Movies"
)

fig2.update_layout(
    template="simple_white",
    title_x=0.5,
    xaxis_title="Runtime (Minutes)",
    yaxis_title="Movies",
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

with st.expander("Insight"):
    st.write(
        """
        Selecting different ratings reveals that runtime varies across
        audience categories. Some mature-rated movies tend to have a
        broader spread of runtimes, while family-oriented titles are
        generally shorter.
        """
    )

st.divider()

# ==================================================
# Directors
# ==================================================

director_df = (
    filtered_df[
        (filtered_df["type"] == "Movie") &
        (filtered_df["director"].notna())
    ]
)

top_directors = (
    director_df["director"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_directors.columns = ["Director", "Movies"]

fig3 = px.bar(
    top_directors,
    x="Movies",
    y="Director",
    orientation="h",
    text="Movies",
    title="Directors with the Most Movies on Netflix"
)

fig3.update_traces(textposition="outside")

fig3.update_layout(
    template="simple_white",
    title_x=0.5,
    height=550,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig3, use_container_width=True)

with st.expander("Insight"):
    st.write(
        """
        Only a small number of directors appear repeatedly in Netflix's
        catalogue. Most directors contribute one or two movies, showing
        that the platform offers content from a broad range of creators.
        """
    )

st.divider()

# ==================================================
# Download
# ==================================================

st.download_button(
    "📥 Download Filtered Dataset",
    filtered_df.to_csv(index=False),
    "content_insights.csv",
    "text/csv"
)