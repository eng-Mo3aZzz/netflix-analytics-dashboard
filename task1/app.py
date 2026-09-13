import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as goS

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon=":clapper:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp{
    background-color:#111111; /* Dark Background */
}

h1,h2,h3,h4,h5,h6{
    color:white;
}

p{
    color:white;
}

[data-testid="stSidebar"]{
    background-color:#191919;
}

[data-testid="metric-container"]{
    background:#1f1f1f;
    border:2px solid #E50914;
    padding:20px;
    border-radius:15px;
}

[data-testid="stMetricValue"]{
    color:#E50914;
    font-size:32px;
}

[data-testid="stMetricLabel"]{
    color:white;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_cleaned.csv")
    df["date_added"] = pd.to_datetime(df["date_added"])
    return df

df = load_data()

# ==================================================
# HEADER
# ==================================================

col1,col2 = st.columns([1,5]) #عشان يقسم الصفحه الى نصفين 

with col1:
    st.image("netflix_logo.png", width=130)

with col2:
    st.title("Netflix Analytics Dashboard")
    st.write("Interactive Dashboard using Streamlit & Plotly")

st.divider()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.image("netflix_logo.png", width=180)

st.sidebar.title("Dashboard Filters")

type_filter = st.sidebar.multiselect(
    "Content Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

country_filter = st.sidebar.multiselect(
    "Country",
    options=sorted(df["country"].unique()),
    default=sorted(df["country"].unique())
)

rating_filter = st.sidebar.multiselect(
    "Rating",
    options=sorted(df["rating"].unique()),
    default=sorted(df["rating"].unique())
)

year_filter = st.sidebar.slider(
    "Release Year",
    int(df.release_year.min()),
    int(df.release_year.max()),
    (
        int(df.release_year.min()),
        int(df.release_year.max())
    )
)

# ==================================================
# FILTER DATA
# ==================================================

filtered_df = df[
    (df["type"].isin(type_filter))
    &
    (df["country"].isin(country_filter))
    &
    (df["rating"].isin(rating_filter))
    &
    (df["release_year"]>=year_filter[0])
    &
    (df["release_year"]<=year_filter[1])
]

# ==================================================
# KPI CARDS
# ==================================================

st.subheader("Dashboard Overview")

k1,k2,k3,k4 = st.columns(4)

k1.metric(
    " Total Titles",
    len(filtered_df)
)

k2.metric(
    " Movies",
    len(filtered_df[filtered_df.type=="Movie"])
)

k3.metric(
    " TV Shows",
    len(filtered_df[filtered_df.type=="TV Show"])
)

k4.metric(
    " Countries",
    filtered_df.country.nunique()
)

st.divider()

# ==================================================
# CHARTS ROW 1
# ==================================================

col1, col2 = st.columns(2, gap="large")

# --------------------------
# Movies vs TV Shows
# --------------------------

with col1:

    fig = px.pie(
        filtered_df,
        names="type",
        hole=0.6,
        color="type",
        color_discrete_sequence=["#E50914", "#564D4D"]
    )

    fig.update_layout(
        title="Movies vs TV Shows",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white",
        title_x=0.25,
        legend_title="Content Type"
    )

    st.plotly_chart(fig, width="stretch")

# --------------------------
# Rating Distribution
# --------------------------

with col2:

    rating = (
        filtered_df["rating"]
        .value_counts()
        .reset_index()
    )

    rating.columns = ["Rating", "Count"]

    fig = px.bar(
        rating,
        x="Rating",
        y="Count",
        color="Count",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        title="Content Rating Distribution",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white",
        title_x=0.2
    )

    st.plotly_chart(fig, width="stretch")

# ==================================================
# CHARTS ROW 2
# ==================================================

col1, col2 = st.columns(2, gap="large")

# --------------------------
# Release Year
# --------------------------

with col1:

    fig = px.histogram(
        filtered_df,
        x="release_year",
        nbins=35,
        color_discrete_sequence=["#E50914"]
    )

    fig.update_layout(
        title="Release Year Distribution",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white",
        title_x=0.25
    )

    st.plotly_chart(fig, width="stretch")

# --------------------------
# Content Added Per Year
# --------------------------

with col2:

    yearly = (
        filtered_df
        .groupby("year_added")
        .size()
        .reset_index(name="Count")
    )

    fig = px.line(
        yearly,
        x="year_added",
        y="Count",
        markers=True
    )

    fig.update_traces(
        line_color="#E50914",
        marker_color="#FFFFFF",
        marker_size=8
    )

    fig.update_layout(
        title="Content Added Per Year",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white",
        title_x=0.25
    )

    st.plotly_chart(fig, width="stretch")
    
    # ==================================================
# CHARTS ROW 3
# ==================================================

col1, col2 = st.columns(2, gap="large")

# ==========================
# Top 10 Countries
# ==========================

with col1:

    country = (
        filtered_df["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country.columns = ["Country", "Count"]

    fig = px.bar(
        country,
        x="Count",
        y="Country",
        orientation="h",
        color="Count",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        title="🌍 Top 10 Countries",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, width="stretch")

# ==========================
# Top Directors
# ==========================

with col2:

    directors = (
        filtered_df[filtered_df["director"] != "Unknown"]["director"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    directors.columns = ["Director", "Count"]

    fig = px.bar(
        directors,
        x="Count",
        y="Director",
        orientation="h",
        color="Count",
        color_continuous_scale="Burg"
    )

    fig.update_layout(
        title=" Top 10 Directors",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, width="stretch")

# ==================================================
# CHARTS ROW 4
# ==================================================

col1, col2 = st.columns(2, gap="large")

# ==========================
# Top Genres
# ==========================

with col1:

    genre = (
        filtered_df["listed_in"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
        .reset_index()
    )

    genre.columns = ["Genre", "Count"]

    fig = px.bar(
        genre,
        x="Genre",
        y="Count",
        color="Count",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(
        title="🎭 Top 10 Genres",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white"
    )

    st.plotly_chart(fig, width="stretch")

# ==========================
# Content Added By Month
# ==========================

with col2:

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    month_df = (
        filtered_df["month_added"]
        .value_counts()
        .reindex(month_order)
        .fillna(0)
        .reset_index()
    )

    month_df.columns = ["Month","Count"]

    fig = px.line(
        month_df,
        x="Month",
        y="Count",
        markers=True
    )

    fig.update_traces(
        line_color="#E50914",
        marker_color="white",
        marker_size=9
    )

    fig.update_layout(
        title="📅 Content Added by Month",
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white"
    )

    st.plotly_chart(fig, width="stretch")
    
    # ==================================================
# DASHBOARD INSIGHTS
# ==================================================

st.divider()
st.subheader("📈 Dashboard Insights")

c1, c2, c3 = st.columns(3)

with c1:
    st.info(f"🎬 Oldest Release Year : {filtered_df['release_year'].min()}")

with c2:
    st.success(f"🔥 Latest Release Year : {filtered_df['release_year'].max()}")

with c3:
    st.warning(f"⭐ Average Release Year : {round(filtered_df['release_year'].mean(),1)}")


# ==================================================
# HEATMAP
# ==================================================

st.divider()
st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include="number")

if len(numeric_df.columns) > 1:

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white"
    )

    st.plotly_chart(fig, width="stretch")


# ==================================================
# DATA TABLE
# ==================================================

st.divider()

st.subheader("📋 Netflix Dataset")

search = st.text_input("🔍 Search by Title")

if search:

    result = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False)
    ]

    st.dataframe(result, width="stretch")

else:

    st.dataframe(filtered_df, width="stretch")


# ==================================================
# DOWNLOAD BUTTON
# ==================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Dataset",
    csv,
    "filtered_netflix.csv",
    "text/csv"
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
"""
<div style='text-align:center'>

<h2 style='color:#E50914'>
Netflix Analytics Dashboard
</h2>

<p>
Developed using
<b>Python</b> •
<b>Streamlit</b> •
<b>Plotly</b>
</p>

<h4>
👨‍💻 Developed by MOAAZ ELDEEP
</h4>

</div>
""",
unsafe_allow_html=True
)