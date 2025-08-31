import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("📊 Reports & Visualization")

if os.path.exists("data/batch_results.csv"):
    df = pd.read_csv("data/batch_results.csv")
    counts = df["Prediction"].value_counts()

    st.write("### Prediction Summary")
    st.bar_chart(counts)

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%")
    st.pyplot(fig)
else:
    st.warning("No report available yet.")