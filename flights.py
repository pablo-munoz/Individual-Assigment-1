import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import time
import random
import os
from streamlit_gsheets import GSheetsConnection

st.title("Airline Passengers Analysis: Which Year Had the Highest Traffic?")

question = "Which year had the highest total number of airline passengers?"
st.subheader(question)

# Create a connection object using Streamlit connections
conn = st.connection("gsheets", type=GSheetsConnection)
# Specify the spreadsheet when calling read()
flights_df = conn.read()


# Prepare data: aggregate total passengers per year
yearly_passengers = flights_df.groupby('year')['passengers'].sum().reset_index()

# Manual refresh button
if st.button("Refresh Data"):
    st.cache_data.clear()  # Clear cache
    st.rerun()  # Reload the app

if 'chart_type' not in st.session_state:
    st.session_state.chart_type = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'chart_displayed' not in st.session_state:
    st.session_state.chart_displayed = False

# Button to randomly select and show one of the two charts
if not st.session_state.chart_displayed:
    if st.button("Show a Chart"):  # first button
        # Randomly pick chart A or B
        st.session_state.chart_type = random.choice(['A', 'B'])

        st.session_state.start_time = time.time()  
        st.session_state.chart_displayed = True
        

# If a chart has been selected and should be displayed:
if st.session_state.chart_displayed and st.session_state.chart_type:
    # Display chart
    if st.session_state.chart_type == 'A':
        st.write("**Chart A: Line Chart of Passenger Growth Over Years**")
        fig = px.line(yearly_passengers, x='year', y='passengers', title="Total Passengers per Year (Line Chart)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("**Chart B: Bar Chart of Total Passengers per Year**")
        fig = px.bar(yearly_passengers, x='year', y='passengers', title="Total Passengers per Year (Bar Chart)")
        st.plotly_chart(fig, use_container_width=True)
    
    # second button to end the question and measure response time
    if st.button("I answered your question"):
        end_time = time.time()
        # Calculate response time in secs
        response_time = end_time - st.session_state.start_time
        # Display the response time
        st.success(f"Your response time: {response_time:.2f} seconds.")
    
