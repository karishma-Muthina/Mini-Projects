import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Google Play Store Data Explorer")

# Load CSV from GitHub
url = "https://raw.githubusercontent.com/your-username/your-repo/main/googleplaystore.csv"

try:
    df = pd.read_csv(url)
    st.success("✅ CSV loaded successfully!")
    
    # Show first few rows
    st.subheader("Preview of Data")
    st.dataframe(df.head())

    # Clean column names
    df.columns = df.columns.str.strip()

    # Rename if needed
    if 'App' not in df.columns and 'App Name' in df.columns:
        df.rename(columns={'App Name': 'App'}, inplace=True)
    elif 'App' not in df.columns:
        st.error("❌ 'App' or 'App Name' column not found.")
        st.stop()

    # Drop duplicates and clean data
    df = df.drop_duplicates(subset='App')
    df = df[df['Rating'].astype(str) != 'NaN']
    df = df[df['Rating'].astype(float) <= 5]

    # Clean installs and reviews
    df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    # Drop missing values from required columns
    df = df[['Category', 'Rating', 'Reviews', 'Installs']].dropna()

    # Grouping for summary
    category_summary = df.groupby('Category').agg({
        'Installs': 'mean',
        'Rating': 'mean',
        'Reviews': 'mean'
    }).sort_values(by='Installs', ascending=False)

    # Plotting
    st.subheader("Top 10 Categories by Average Installs")

    fig, ax = plt.subplots(figsize=(10, 6))
    category_summary['Installs'].head(10).plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Top 10 Categories by Average Installs')
    ax.set_ylabel('Average Installs')
    ax.set_xlabel('Category')
    ax.set_xticklabels(category_summary.head(10).index, rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Display summary
    st.subheader("Top Categories Summary Table")
    st.dataframe(category_summary.reset_index().head(10))

except Exception as e:
    st.error(f"❌ Failed to load or process CSV: {e}")
