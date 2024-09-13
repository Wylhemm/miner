import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from furl import furl

def get_base_domain(url):
    """Extract the base domain from a URL."""
    return furl(url).origin

def find_social_links(url, timeout=10):
    """Scrape the website to find Instagram handle and Facebook link."""
    start_time = time.time()
    social_links = {'instagram': None, 'facebook': None}
    try:
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            if time.time() - start_time > timeout:
                print(f"Timeout reached while searching for social links on {url}")
                return social_links
            href = a_tag['href']
            if 'instagram.com' in href and not social_links['instagram']:
                social_links['instagram'] = urlparse(href).path.strip('/').split('/')[0]
            elif 'facebook.com' in href and not social_links['facebook']:
                social_links['facebook'] = href
            if all(social_links.values()):
                break
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
    return social_links