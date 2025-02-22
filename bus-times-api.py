import requests
from bs4 import BeautifulSoup
import re

def fetch_departures(url, headers, service_filter="SHTL"):

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    p_tags = soup.find_all('p', class_='sr-only')

    filtered_departures = []

    for p_tag in p_tags:
        text = p_tag.get_text(strip=True)

        # Extract details using regex
        match = re.search(r"Service - (.+?)\. Destination - (.+?)\. Departure time - (.+?)\.", text)
        if match:
            service = match.group(1)
            destination = match.group(2)
            departure_time = match.group(3)

            # Filter based on the service code
            if service == service_filter:
                filtered_departures.append({
                    "Service": service,
                    "Destination": destination,
                    "Departure Time": departure_time
                })

    return filtered_departures


def display_departures(departures):

    if not departures:
        print("No departures found for the specified service.")
        return

    for idx, departure in enumerate(departures, start=1):
        print(f"Departure {idx}:")
        print(f"  Service: {departure['Service']}")
        print(f"  Destination: {departure['Destination']}")
        print(f"  Departure Time: {departure['Departure Time']}")
        print("-" * 40)


# Main execution
if __name__ == "__main__":
    url = "https://www.intalink.org.uk/stops/210021608014"
    headers = {
        "cookie": "passenger-favourites-0=%7B%22device%22%3A%224c744f4f355e65c68b071b1eb191b439%22%2C%22user%22%3Anull%2C%22lastSync%22%3Anull%2C%22favourites%22%3A%5B%5D%7D",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
        "referer": url,
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    # Fetch and display departures filtered by "SHTL"
    departures = fetch_departures(url, headers, service_filter="SHTL")
    display_departures(departures)

    
