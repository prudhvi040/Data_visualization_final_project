from pathlib import Path

import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """
    Load and preprocess the Netflix dataset.
    """

    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "netflix_titles.csv"
    )

    df = pd.read_csv(data_path)

    # Convert dates
    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    # Date features
    df["added_year"] = df["date_added"].dt.year
    df["added_month"] = df["date_added"].dt.month_name()

    # Duration
    df["duration_num"] = (
        df["duration"]
        .str.extract(r"(\d+)")
        .astype(float)
    )

    df["duration_unit"] = (
        df["duration"]
        .str.extract(r"([A-Za-z]+)")
    )

    return df


def apply_sidebar_filters(df):
    """
    Create sidebar filters shared across all pages.
    """

    st.sidebar.header("Dashboard Filters")

    content_types = sorted(df["type"].dropna().unique())

    selected_types = st.sidebar.multiselect(
        "Content Type",
        options=content_types,
        default=content_types
    )

    min_year = int(df["added_year"].dropna().min())
    max_year = int(df["added_year"].dropna().max())

    selected_years = st.sidebar.slider(
        "Year Added",
        min_year,
        max_year,
        (min_year, max_year)
    )

    filtered = df[
        (df["type"].isin(selected_types))
        &
        (df["added_year"].between(
            selected_years[0],
            selected_years[1]
        ))
    ]

    return filtered