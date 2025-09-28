import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df = df.dropna(subset=["title", "publish_time"]).copy()
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = df["publish_time"].dt.year
    df["abstract_word_count"] = df["abstract"].fillna("").apply(lambda x: len(x.split()))
    return df

df = load_data()

# App title
st.title("📊 CORD-19 Data Explorer")
st.write("Explore COVID-19 research publications interactively")

# Filter by year range
min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.slider("Select year range", min_year, max_year, (2020, 2021))
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Publications by year
st.subheader("Publications by Year")
year_counts = filtered_df["year"].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax, palette="Blues_d")
ax.set_title("Number of Publications by Year")
st.pyplot(fig)

# Top Journals
st.subheader("Top Journals")
top_journals = filtered_df["journal"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax, palette="Greens_d")
ax.set_title("Top Journals")
st.pyplot(fig)

# Word Cloud
st.subheader("Word Cloud of Titles")
text = " ".join(filtered_df["title"].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Show sample data
st.subheader("Sample Data")
st.write(filtered_df.head(10))
