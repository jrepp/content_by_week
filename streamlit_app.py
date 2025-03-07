import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = "file_by_week_prod.csv"
df = pd.read_csv(file_path)

# Rename columns
df.columns = ["timestamp", "count", "content_type"]
df["timestamp"] = pd.to_datetime(df["timestamp"])

df["week"] = df["timestamp"].dt.to_period("W")
weekly_data = df.groupby(["week", "content_type"])["count"].sum().reset_index()
weekly_data["week"] = weekly_data["week"].astype(str)

# Streamlit UI
st.title("Content Type Distribution by Week")
st.sidebar.header("Filters")

# Select content types to display
all_content_types = weekly_data["content_type"].unique().tolist()
selected_types = st.sidebar.multiselect("Select content types:", all_content_types, default=all_content_types)
filtered_data = weekly_data[weekly_data["content_type"].isin(selected_types)]

# Plot using Plotly
st.subheader("Stacked Bar Chart of Content Types by Week")
fig = px.bar(filtered_data, x="week", y="count", color="content_type", title="Content Types by Week",
             labels={"week": "Week", "count": "Count", "content_type": "Content Type"},
             barmode="stack")
st.plotly_chart(fig)
