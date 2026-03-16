from processing.event_processor import process_events, display_processed_events
from scoring.risk_scoring import calculate_country_risk, display_country_risk
import feedparser

RSS_FEEDS={
    "BBC World":"https://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera":"https://www.aljazeera.com/xml/rss/all.xml",
    "CNN World":"http://rss.cnn.com/rss/edition_world.rss"
}

def fetch_feed(source_name, url):
    print(f"Fetching RSS feed from {source_name}...")

    feed=feedparser.parse(url)
    events=[]

    for entry in feed.entries[:10]:
        event={
            "source":source_name,
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")
        }
        events.append(event)
    
    return events

def fetch_all_feeds():
    all_events=[]
    for source, url in RSS_FEEDS.items():
        events=fetch_feed(source, url)
        all_events.extend(events)
    
    return all_events

def display_events(events):
    print("\n Latest Global Events")
    print("-" *50)

    for i,event in enumerate(events, 1):
        print(f"\nEvent {i}")
        print(f"Source: {event['source']}")
        print(f"Title: {event['title']}")
        print(f"Published: {event['published']}")
        print(f"Link: {event['link']}")

if __name__ == "__main__":
    events= fetch_all_feeds()
    processed= process_events(events)
    display_processed_events(processed)
    country_scores= calculate_country_risk(processed)
    display_country_risk(country_scores)