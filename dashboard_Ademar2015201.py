#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np


# In[2]:


data = pd.read_csv("fremont_bridge_clean.csv")


# In[3]:


data["Date"] = pd.to_datetime(data["Date"])


# In[4]:


data["Year"] = data["Date"].dt.year
data["Month"] = data["Date"].dt.month_name()
data["Weekday"] = data["Date"].dt.day_name()
data["Hour"] = data["Date"].dt.hour


# In[5]:


st.title("🚴 Fremont Bridge Cyclist Count Dashboard")
st.image("fremont_bridge.jpg", width=700)

st.markdown(
    "Explore cyclist activity on the East and West pathways using interactive filters."
)


st.sidebar.header("Filter Options")

years = ["All"] + sorted(data["Year"].unique().tolist())

selected_year = st.sidebar.selectbox(
    "Year",
    years
)

months = [
    "All",
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
]

selected_month = st.sidebar.selectbox(
    "Month",
    months
)
weekday_order = [
    "All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

selected_weekday = st.sidebar.selectbox(
    "Weekday",
    weekday_order
)

filtered_data = data.copy()

if selected_year != "All":
    filtered_data = filtered_data[
        filtered_data["Year"] == selected_year
    ]

if selected_month != "All":
    filtered_data = filtered_data[
        filtered_data["Month"] == selected_month
    ]

if selected_weekday != "All":
    filtered_data = filtered_data[
        filtered_data["Weekday"] == selected_weekday
    ]

east_total = filtered_data["EastSidewalk"].sum()
west_total = filtered_data["WestSidewalk"].sum()
total = east_total + west_total

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🚴 East Sidewalk", f"{int(east_total):,}")

with col2:
    st.metric("🚴 West Sidewalk", f"{int(west_total):,}")

with col3:
    st.metric("🔥 Total Cyclists", f"{int(total):,}")

hourly_data = (
    filtered_data
    .groupby("Hour")[["EastSidewalk", "WestSidewalk"]]
    .sum()
    .reset_index()
)
import plotly.express as px

fig = px.line(
    hourly_data,
    x="Hour",
    y=["EastSidewalk", "WestSidewalk"],
    title="East vs West Cyclists by Hour",
    color_discrete_sequence=["#1f77b4", "#d62728"]
)

st.plotly_chart(fig, use_container_width=True)

weekday_data = (
    filtered_data
    .groupby("Weekday")[["EastSidewalk", "WestSidewalk"]]
    .sum()
    .reindex(weekday_order)
    .reset_index()
)
fig2 = px.bar(
    weekday_data,
    x="Weekday",
    y=["EastSidewalk", "WestSidewalk"],
    barmode="group",
    title="East vs West Cyclists by Weekday",
    color_discrete_sequence=["#1f77b4", "#d62728"]
)


hour_total = (
    filtered_data
    .groupby("Hour")["StTotal"]
    .sum()
    .reset_index()
)
fig3 = px.bar(
    hour_total,
    x="Hour",
    y="StTotal",
    title="Total Cyclists by Hour",
    color_discrete_sequence=["blue", "red"]
)


left, right = st.columns(2)

with left:
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.plotly_chart(fig3, use_container_width=True)