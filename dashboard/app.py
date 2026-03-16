import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_autorefresh import st_autorefresh
from ingestion.rss_fetcher import fetch_all_feeds
from processing.event_processor import process_events
from processing.article_extractor import extract_article_content
from scoring.risk_scoring import calculate_country_risk
from scoring.trend_detection import detect_trends, get_trending_locations

# Page Configuration
st.set_page_config(page_title="World Monitor", layout="wide")
st.title("Global Event Monitor")

st_autorefresh(interval=60000, key="datarefresh")

# Fetch and Process Data
@st.cache_data(ttl=60)
def load_events():
    raw_events= fetch_all_feeds()
    return process_events(raw_events)

processed_events= load_events()
#st.write(processed_events[:5])
df= pd.DataFrame(processed_events)

# Sidebar Filters
st.sidebar.header("Filters")

event_filter= st.sidebar.multiselect(
    "Event Type",
    options=df["event_type"].unique(),
    default=df["event_type"].unique()
)

severity_filter= st.sidebar.multiselect(
    "Severity",
    options=df["severity"].unique(),
    default=df["severity"].unique()
)

filtered_df= df[
    (df["event_type"].isin(event_filter)) &
    (df["severity"].isin(severity_filter))
]

location_counts= detect_trends(filtered_df.to_dict("records"))
trending_locations= get_trending_locations(location_counts)

# Latest Events Table
st.subheader("Latest Global Events")

st.dataframe(
    filtered_df[["title", "location", "country", "event_type", "severity", "source"]],
    use_container_width=True
)

# Risk Scoring
country_scores= calculate_country_risk(filtered_df.to_dict("records"))

risk_df= pd.DataFrame(
    list(country_scores.items()),
    columns=["country", "risk_score"]
)

st.subheader("Country Risk Scores")

st.dataframe(
    risk_df.sort_values("risk_score", ascending=False),
    use_container_width=True
)

# Global Event Map
map_df= filtered_df.dropna(subset=["latitude", "longitude"])

st.subheader("Global Event Map")

fig= px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    color="severity",
    hover_name="title",
    projection="natural earth",
    color_discrete_map={
        "high": "red",
        "medium": "orange",
        "low": "green"
    },
)

st.plotly_chart(fig, use_container_width=True)

# Global Risk Heatmap
st.subheader("Global Risk Heatmap")

fig_heatmap = px.choropleth(
    risk_df,
    locations="country",
    locationmode="country names",
    color="risk_score",
    color_continuous_scale="Reds",
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.subheader("Trending Regions")

if trending_locations:
    trend_df=pd.DataFrame(
        list(trending_locations.items()),
        columns=["country", "event_count"]
    )

    st.dataframe(trend_df.sort_values("event_count",ascending=False))

else:
    st.write("No trends detected.")

# Read the Articles
st.subheader("Read Article")

selected_article= st.selectbox(
    "Choose an article to read",
    ["Select an article..."] + filtered_df["title"].tolist()
)

if selected_article != "Select an article...":

    article_row= filtered_df[filtered_df["title"]== selected_article].iloc[0]

    article_data= extract_article_content(article_row["link"])

    st.markdown(f"### {article_row['title']}")
    st.write(article_data["text"])