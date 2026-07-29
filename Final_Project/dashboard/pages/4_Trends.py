import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Release Trends", layout="wide")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data()
filtered_df = apply_sidebar_filters(df)

st.title("📅 Release Trends")

st.write(
    """
    This section explores when Netflix adds content throughout the year
    and how the balance between Movies and TV Shows has changed over time.
    """
)

st.divider()

# ==================================================
# Monthly Additions
# ==================================================

monthly = (
    filtered_df.groupby("added_month")
    .size()
    .reset_index(name="Titles")
)

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly["added_month"] = pd.Categorical(
    monthly["added_month"],
    categories=month_order,
    ordered=True
)

monthly = monthly.sort_values("added_month")

fig = px.bar(
    monthly,
    x="added_month",
    y="Titles",
    title="Monthly Content Additions"
)

fig.update_layout(
    template="simple_white",
    title_x=0.5,
    xaxis_title="Month",
    yaxis_title="Titles Added",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Insight"):
    st.write(
        """
        Netflix releases content throughout the year, although some
        months consistently receive more additions than others. This
        suggests planned release schedules rather than random publishing.
        """
    )

st.divider()

# ==================================================
# Evolution of Content Types
# ==================================================

type_year = (
    filtered_df
    .groupby(["added_year", "type"])
    .size()
    .reset_index(name="Titles")
)

fig2 = px.area(
    type_year,
    x="added_year",
    y="Titles",
    color="type",
    title="Evolution of Movies and TV Shows",
    color_discrete_map={
        "Movie": "#1f77b4",
        "TV Show": "#ff7f0e"
    }
)

fig2.update_layout(
    template="simple_white",
    title_x=0.5,
    xaxis_title="Year Added",
    yaxis_title="Titles",
    legend_title="Content Type",
    height=550
)

st.plotly_chart(fig2, use_container_width=True)

with st.expander("Insight"):
    st.write(
        """
        Although Movies remain a substantial part of Netflix's catalogue,
        the number of TV Shows has grown steadily over time. This reflects
        Netflix's increasing investment in original series and long-form
        content.
        """
    )

st.divider()

# ==================================================
# Year Explorer
# ==================================================

available_years = sorted(
    filtered_df["added_year"].dropna().unique()
)

selected_year = st.selectbox(
    "Explore a specific year",
    available_years
)

year_df = filtered_df[
    filtered_df["added_year"] == selected_year
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Titles",
    len(year_df)
)

col2.metric(
    "Movies",
    (year_df["type"] == "Movie").sum()
)

col3.metric(
    "TV Shows",
    (year_df["type"] == "TV Show").sum()
)

with st.expander("View Titles Added"):
    st.dataframe(
        year_df[
            [
                "title",
                "type",
                "country",
                "rating",
                "listed_in"
            ]
        ],
        use_container_width=True
    )

st.divider()

st.download_button(
    "📥 Download Filtered Dataset",
    filtered_df.to_csv(index=False),
    "release_trends.csv",
    "text/csv"
)