from collections import defaultdict

def detect_trends(events):
    location_counts = defaultdict(int)
    for event in events:
        location=event.get("country", "Unknown")
        if location == "Unknown":
            continue

        location_counts[location]+=1
    
    return location_counts

def get_trending_locations(location_counts, threshold=3):
    trending={}

    for location, count in location_counts.items():
        if count >=threshold:
            trending[location]=count
    return trending