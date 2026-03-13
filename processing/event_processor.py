from processing.geocoder import get_coordinates, get_country_from_coordinates
from processing.event_classifier import classify_event_ai
import spacy
import re

nlp= spacy.load("en_core_web_sm")

EVENT_KEYWORDS={
    "conflict":[
        "war", "missile", "attack", "drone", "strike", "bomb", "military",
        "airstrike", "explosion", "battle"
    ],
    "protest":[
        "protest", "demonstration", "riot", "march", "strike", "unrest"
    ],
    "disaster":[
        "earthquake", "flood", "wildfire", "storm", "hurricane", "tsunami",
        "landslide"
    ],
    "politics":[
        "election", "government", "parliament", "sanction", "policy",
        "president", "prime minister"
    ],
    "economy":[
        "inflation", "recession", "stock", "market", "trade", "economic"
    ]
}

SEVERITY_KEYWORDS={
    "high":["explosion", "missile", "bomb", "airstrike", "war", "attack"],
    "medium":["protest", "riot", "demonstration", "strike"],
    "low":["election", "policy", "government", "trade"]
}

SEVERITY_WEIGHTS={
    "explosion":5,
    "missile":5,
    "bomb":5,
    "airstrike":5,
    "war":4,
    "attack":4,
    "drone":3,
    "military":3,
    "riot":3,
    "protest":2,
    "demonstration":2,
    "policy":1,
    "election":1
}

EVENT_SEVERITY_BASE={
    "conflict":3,
    "disaster":3,
    "protest":2,
    "politics":1,
    "economy":1,
    "other":1
}

def classify_event(title, summary):
    text= f"{title} {summary}".lower()
    scores= {event_type: 0 for event_type in EVENT_KEYWORDS}

    for event_type, keywords in EVENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[event_type]+= 1

    best_category= max(scores, key=scores.get)

    if scores[best_category]== 0:
        return "other"

    return best_category

def determine_severity(title, summary, event_type):
    text= f"{title} {summary}".lower()
    score= 0

    for word, weight in SEVERITY_WEIGHTS.items():
        if word in text:
            score+= weight

    score+= EVENT_SEVERITY_BASE.get(event_type, 1)

    if score >= 7:
        return "high"
    elif score >= 4:
        return "medium"
    else:
        return "low"

def extract_location(title, summary):
    text= f"{title} {summary}"

    doc= nlp(text)

    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text

    return "Unknown"

def process_events(events):
    processed_events= []

    for event in events:

        event_type= classify_event_ai(event["title"], event["summary"])
        severity= determine_severity(event["title"], event["summary"], event_type)
        location= extract_location(event["title"], event["summary"])
        
        if location != "Unknown":
            lat, lon= get_coordinates(location)

            if lat and lon:
                country= get_country_from_coordinates(lat, lon)
            else:
                country= "Unknown"
        else:
            lat, lon= None, None
            country= "Unknown"

        processed_event={
            "title": event["title"],
            "source": event["source"],
            "published": event["published"],
            "link": event["link"],
            "event_type": event_type,
            "severity": severity,
            "location": location,
            "country": country,
            "latitude": lat,
            "longitude": lon
        }

        processed_events.append(processed_event)

    return processed_events


def display_processed_events(events):
    print("\nProcessed Intelligence Events\n")
    print("=" * 60)

    for i, event in enumerate(events, 1):
        print(f"\nEvent {i}")
        print(f"Title: {event['title']}")
        print(f"Source: {event['source']}")
        print(f"Location: {event['location']}")
        print(f"Event Type: {event['event_type']}")
        print(f"Severity: {event['severity']}")