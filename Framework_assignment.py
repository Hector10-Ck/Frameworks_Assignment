# 🧠 CORD-19 Metadata Analysis and Visualization
# Author: Hector
# Frameworks Assignment

# --- 📦 Import Required Libraries ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from wordcloud import WordCloud

# --- 📥 Load Dataset ---
# Replace with actual path to metadata.csv
df = pd.read_csv(r"C:\Users\SILVERETCH\Framework assignment\metadata.csv")

# --- 🔍 Basic Exploration ---
print("🔹 First 5 rows:")
print(df.head())

print("\n🔹 Shape of DataFrame:", df.shape)
print("\n🔹 Column Data Types:")
print(df.dtypes)

print("\n🔹 Missing Values:")
print(df.isnull().sum())

print("\n🔹 Summary Statistics:")
print(df.describe())

# --- 🧹 Data Cleaning ---
# Drop columns with too many missing values
df_clean = df.dropna(axis=1, thresh=0.5 * len(df))

# Fill missing titles or journals with placeholder
df_clean['title'] = df_clean['title'].fillna('No Title')
df_clean['journal'] = df_clean['journal'].fillna('Unknown Journal')

# Convert publication date
if 'publish_time' in df_clean.columns:
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
    df_clean['year'] = df_clean['publish_time'].dt.year

# Create new column: abstract word count
if 'abstract' in df_clean.columns:
    df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').apply(lambda x: len(x.split()))

# --- 📊 Data Analysis ---
# Count papers by year
papers_per_year = df_clean['year'].value_counts().sort_index()

# Top journals
top_journals = df_clean['journal'].value_counts().head(10)

# --- 🧠 Simple Word Frequency ---
titles = " ".join(df_clean['title'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)

# --- 📈 Visualizations ---
plt.figure(figsize=(8,5))
papers_per_year.plot(kind='bar')
plt.title('Number of Publications by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("publications_by_year.png")

plt.figure(figsize=(8,5))
top_journals.plot(kind='barh')
plt.title('Top 10 Journals Publishing COVID-19 Research')
plt.xlabel('Count')
plt.ylabel('Journal')
plt.tight_layout()
plt.savefig("top_journals.png")

plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Frequent Words in Titles")
plt.tight_layout()
plt.savefig("wordcloud_titles.png")

# --- 🌐 Streamlit App ---
st.title("📊 CORD-19 Data Explorer")
st.write("Explore COVID-19 research metadata interactively")

st.subheader("🧠 Sample of the Data")
st.dataframe(df_clean.head(10))

# Year filter
year_range = st.slider("Select Year Range", 2019, 2025, (2020, 2021))
filtered = df_clean[(df_clean['year'] >= year_range[0]) & (df_clean['year'] <= year_range[1])]

st.subheader("📈 Publications by Year")
st.bar_chart(filtered['year'].value_counts().sort_index())

st.subheader("🏢 Top Journals")
st.bar_chart(filtered['journal'].value_counts().head(10))

st.subheader("☁️ Word Cloud of Titles")
st.image("wordcloud_titles.png")

st.write("✅ Analysis complete! Use filters to explore different years.")