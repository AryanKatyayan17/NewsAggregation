from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_classifier():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

classifier=load_classifier()

EVENT_LABELS=[
    "conflict",
    "protest",
    "disaster",
    "politics",
    "economy"
]

def classify_event_ai(title,summary):
    text=f"{title}. {summary}"
    result=classifier(text,EVENT_LABELS)
    return result["labels"][0]
