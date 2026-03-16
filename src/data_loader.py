"""
Data loading and cleaning pipeline for UCDP GED conflict event data.

This module provides reusable functions for loading, cleaning, and filtering
UCDP data for the Ethiopia/Tigray conflict analysis (Nov 2020 - Nov 2022).

Usage:
    from src.data_loader import load_ucdp_data, filter_ethiopia_events
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_ucdp_data(filepath: str) -> pd.DataFrame:
    """
    Load UCDP GED CSV data and perform initial cleaning.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(
            f"Data file not found at {filepath}. "
            "Download UCDP GED from https://ucdp.uu.se/downloads"
        )

    df = pd.read_csv(filepath, low_memory=False)

    # Parse dates
    df["date_start"] = pd.to_datetime(df["date_start"])
    df["date_end"] = pd.to_datetime(df["date_end"])

    # Report missing coordinates before dropping
    missing_coords = df[["latitude", "longitude"]].isnull().any(axis=1).sum()
    if missing_coords > 0:
        print(f"Warning: Dropping {missing_coords} rows with missing coordinates "
              f"({missing_coords / len(df) * 100:.1f}% of data)")

    df = df.dropna(subset=["latitude", "longitude"])

    # Add derived time columns
    df["year"] = df["date_start"].dt.year
    df["month"] = df["date_start"].dt.month
    df["yearmonth"] = df["date_start"].dt.to_period("M")

    print(f"Loaded {len(df)} events from {df['date_start'].min().date()} "
          f"to {df['date_start'].max().date()}")

    return df


def filter_ethiopia_events(
    df: pd.DataFrame,
    start_date: str = "2020-11-01",
    end_date: str = "2022-11-30",
    type_of_violence: int = None,
    country: str = "Ethiopia",
) -> pd.DataFrame:
    """
    Filter UCDP data to Ethiopia and the Tigray conflict period.

    type_of_violence codes:
        1 = state-based conflict
        2 = non-state conflict
        3 = one-sided violence (violence against civilians)
    """
    mask = (
        (df["country"] == country)
        & (df["date_start"] >= pd.Timestamp(start_date))
        & (df["date_start"] <= pd.Timestamp(end_date))
    )

    if type_of_violence is not None:
        mask = mask & (df["type_of_violence"] == type_of_violence)

    filtered = df[mask].copy()

    type_labels = {1: "state-based", 2: "non-state", 3: "one-sided (civilians)"}
    print(f"Filtered to {len(filtered)} events in {country}")
    if type_of_violence:
        print(f"  Violence type: {type_labels.get(type_of_violence, type_of_violence)}")

    return filtered


def get_event_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summary table of event counts and fatalities by violence type.
    """
    type_labels = {1: "State-based conflict", 2: "Non-state conflict", 3: "One-sided violence"}
    summary = (
        df.groupby("type_of_violence")
        .agg(
            event_count=("type_of_violence", "size"),
            best_fatality_estimate=("best", "sum"),
            low_fatality_estimate=("low", "sum"),
            high_fatality_estimate=("high", "sum"),
        )
        .sort_values("event_count", ascending=False)
        .reset_index()
    )
    summary["violence_label"] = summary["type_of_violence"].map(type_labels)
    summary["pct_of_events"] = (
        summary["event_count"] / summary["event_count"].sum() * 100
    ).round(1)

    return summary


def get_monthly_counts(df: pd.DataFrame, by_type: bool = False) -> pd.DataFrame:
    """
    Aggregate event counts by month.
    """
    if by_type:
        counts = (
            df.groupby(["yearmonth", "type_of_violence"])
            .size()
            .reset_index(name="event_count")
        )
    else:
        counts = (
            df.groupby("yearmonth")
            .size()
            .reset_index(name="event_count")
        )

    counts["date"] = counts["yearmonth"].dt.to_timestamp()
    return counts


def get_actor_summary(df: pd.DataFrame, actor_col: str = "side_a", top_n: int = 15) -> pd.DataFrame:
    """
    Summarize the most active actors by event count and fatalities.

    UCDP uses side_a (typically government) and side_b (typically rebel/opposition).
    """
    summary = (
        df.groupby(actor_col)
        .agg(
            event_count=(actor_col, "size"),
            total_fatalities=("best", "sum"),
        )
        .sort_values("event_count", ascending=False)
        .head(top_n)
        .reset_index()
    )
    return summary