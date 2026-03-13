from collections import defaultdict

EVENT_RISK_WEIGHTS={
    "conflict":5,
    "protest":3,
    "disaster":4,
    "politics":2,
    "economy":1,
    "other":1
}

SEVERITY_MULTIPLIERS={
    "high":3,
    "medium":2,
    "low":1
}

def calculate_event_risk(event):
    base= EVENT_RISK_WEIGHTS.get(event["event_type"], 1)
    multiplier= SEVERITY_MULTIPLIERS.get(event["severity"], 1)

    return base * multiplier

def calculate_country_risk(events):
    country_scores= defaultdict(int)

    for event in events:

        location= event.get("country", "Unknown")

        if location== "Unknown":
            continue

        risk= calculate_event_risk(event)

        country_scores[location] += risk

    return country_scores


def display_country_risk(country_scores):

    print("\nCountry Risk Scores\n")
    print("=" * 50)

    sorted_scores= sorted(country_scores.items(), key=lambda x: x[1], reverse=True)

    for country,score in sorted_scores:
        print(f"{country}: {score}")