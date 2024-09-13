import requests

def is_domain_in_pocketbase(website):
    """Check if the domain already exists in PocketBase."""
    url = f"http://198.74.53.241/api/collections/Leads/records?filter=(website='{website}')"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])  # If items list is empty, return False
    except requests.RequestException as e:
        print(f"Error checking domain in PocketBase: {e}")
        return True  # Assume it exists if there's an error

def send_to_pocketbase(business_name, website, ig_handle, facebook_link):
    """Send successful lookup to PocketBase if not already present."""
    if is_domain_in_pocketbase(website):
        print(f"Domain {website} already exists in PocketBase, skipping...")
        return

    url = "http://198.74.53.241/api/collections/Leads/records"
    data = {
        "business_name": business_name,
        "website": website,
        "ig_handle": ig_handle,
        "facebook_link": facebook_link
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(f"Successfully sent data for {business_name} to PocketBase")
    except requests.RequestException as e:
        print(f"Error sending data to PocketBase: {e}")