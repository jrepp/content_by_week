import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = "file_by_week_prod.csv"
df = pd.read_csv(file_path)

# Rename columns
df.columns = ["timestamp", "count", "content_type"]
df["timestamp"] = pd.to_datetime(df["timestamp"])

df["week"] = df["timestamp"].dt.to_period("W")
weekly_data = df.groupby(["week", "content_type"])["count"].sum().unstack(fill_value=0)
weekly_data.index = weekly_data.index.astype(str)

# Streamlit UI
st.title("Content Type Distribution by Week")
st.sidebar.header("Filters")

# Select content types to display
all_content_types = weekly_data.columns.tolist()
selected_types = st.sidebar.multiselect("Select content types:", all_content_types, default=all_content_types)
filtered_data = weekly_data[selected_types]

# Plot
st.subheader("Stacked Bar Chart of Content Types by Week")
fig, ax = plt.subplots(figsize=(12, 6))
filtered_data.plot(kind="bar", stacked=True, ax=ax)
ax.set_xlabel("Week")
ax.set_ylabel("Count")
ax.set_title("Content Types by Week")
plt.xticks(rotation=45)
plt.legend(title="Content Type", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)
